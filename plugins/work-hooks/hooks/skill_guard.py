#!/usr/bin/env python3
"""Skill-Wächter v1: prüft vor bzw. nach einer Aktion, ob der zuständige Skill geladen ist (docs/skill-guard-v1.md).

Hook für Claude Code:
- PreToolUse  → Regeln mit modus "blocken": fehlt der Pflicht-Skill, wird die Aktion abgelehnt (Exit 2, Begründung
  auf stderr; Claude sieht sie und lädt den Skill nach).
- PostToolUse → Regeln mit modus "warnen": fehlt der Pflicht-Skill, bekommt Claude nach der Aktion einen Hinweis
  (additionalContext).
Die Regeln stehen in regeln.json neben diesem Skript; skill-auswertung schärft sie nach. Jede Entscheidung landet als
Ereignis "guard" im Skill-Log (<SKILL_LOG_DIR>/<JJJJ-MM>.jsonl).

Ein Fehler im Skript blockiert nie: Exit 0 ohne Ausgabe. Abschalten: Umgebungsvariable SKILL_GUARD=aus.

Umgebungsvariablen (optional):
  SKILL_GUARD        "aus" = nichts prüfen
  SKILL_GUARD_RULES  Pfad zur Regeldatei (Standard: regeln.json neben dem Skript)
  SKILL_LOG_DIR      Ablage des Skill-Logs (Standard: ~/.claude/skill-log)
  SKILL_LOG_HOST     Name des Rechners im Log (Standard: Hostname)
"""

import datetime
import fnmatch
import json
import os
import re
import shlex
import socket
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
FILE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
_CLICKUP_WRITE = re.compile(r"^mcp__.*clickup.*__clickup_(create|update|delete|merge|move|add|remove|attach|set)",
                            re.I)
_GIT_COMMIT = re.compile(r"\bgit\b(?:\s+-C\s+\S+)?\s+commit\b")
_REDIRECT = re.compile(r"(?:^|[^0-9&<>])>>?\s*([^\s;|&<>()]+)")
_TEE = re.compile(r"\btee\s+(?:-a\s+)?([^\s;|&<>()]+)")
_SED_I = re.compile(r"\bsed\s+(?:-[^i\s]*\s+)*-i\S*\s+(.*)")
_CP_MV = re.compile(r"^\s*(?:cp|mv|install)\s+(.*)")
_PY_WRITE = re.compile(r"open\([^)]*['\"][wax]b?['\"]|\.write_text\(|\.write\(|shutil\.(?:copy|move)")
_QUOTED_FILE = re.compile(r"['\"]([\w./~-]*[\w-]\.[A-Za-z0-9]{1,5}|[\w./~-]*/mockups/[\w./-]+)['\"]")
_SEGMENT = re.compile(r"\s*(?:;|&&|\|\||\||\n)\s*")
_COMMAND_NAME = re.compile(r"<command-name>/?([\w:.-]+)</command-name>")
_PROJECT_ID = re.compile(r"^\s*-\s*Projekt-ID:\s*(\S+)", re.M)


def short(name):
    return (name or "").split(":")[-1]


def load_rules(path=None):
    path = path or os.environ.get("SKILL_GUARD_RULES") or os.path.join(HERE, "regeln.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def project_of(cwd):
    """Projekt-ID aus dem Skill-Profil der nächsten CLAUDE.md ab cwd nach oben, sonst der Ordnername."""
    path = os.path.abspath(cwd or os.getcwd())
    start = path
    while True:
        claude_md = os.path.join(path, "CLAUDE.md")
        if os.path.isfile(claude_md):
            try:
                with open(claude_md, encoding="utf-8") as fh:
                    match = _PROJECT_ID.search(fh.read())
                if match:
                    return match.group(1)
            except OSError:
                pass
        parent = os.path.dirname(path)
        if parent == path:
            return os.path.basename(start) or start
        path = parent


def transcripts(data):
    """Transcript der Aktion und, bei Subagenten, das der Hauptsitzung."""
    paths = []
    tp = data.get("transcript_path")
    if tp:
        paths.append(tp)
        if "/subagents/" in tp:
            paths.append(tp.split("/subagents/")[0] + ".jsonl")
        session = data.get("session_id")
        if session:
            folder = os.path.dirname(tp.split("/subagents/")[0]) if "/subagents/" in tp else os.path.dirname(tp)
            main = os.path.join(folder, session + ".jsonl")
            if main not in paths:
                paths.append(main)
    return [p for p in paths if os.path.isfile(p)]


def loaded_skills(paths):
    """Alle in den Transcripts geladenen Skills: Skill-Aufrufe, Slash-Befehle, Anhang invoked_skills (Compaction)."""
    found = set()
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    if '"Skill"' not in line and "command-name" not in line and "invoked_skills" not in line:
                        continue
                    try:
                        msg = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    attachment = msg.get("attachment")
                    if isinstance(attachment, dict) and attachment.get("type") == "invoked_skills":
                        # nach einer Compaction legt Claude Code die geladenen Skills als Anhang ab
                        found.update(short(s.get("name")) for s in attachment.get("skills") or [])
                        continue
                    content = (msg.get("message") or {}).get("content")
                    if isinstance(content, str):
                        found.update(short(m) for m in _COMMAND_NAME.findall(content))
                    elif isinstance(content, list):
                        for block in content:
                            if block.get("type") == "tool_use" and block.get("name") == "Skill":
                                found.add(short((block.get("input") or {}).get("skill")))
                            elif block.get("type") == "text":
                                found.update(short(m) for m in _COMMAND_NAME.findall(block.get("text") or ""))
        except OSError:
            continue
    found.discard("")
    return found


def bash_targets(command):
    """Dateien, die ein Shell-Befehl schreibt: Umleitungen, tee, sed -i, Ziel von cp/mv, Schreiben in Python-Heredocs."""
    targets = []
    heredoc = command.find("<<")
    shell = command if heredoc < 0 else command[:heredoc] + command[heredoc:].split("\n", 1)[0]
    targets += _REDIRECT.findall(shell)
    targets += _TEE.findall(shell)
    for segment in _SEGMENT.split(shell):
        match = _SED_I.search(segment)
        if match:
            try:
                args = shlex.split(match.group(1))
            except ValueError:
                args = match.group(1).split()
            targets += [a for a in args[1:] if not a.startswith("-")]
        match = _CP_MV.match(segment)
        if match:
            try:
                args = [a for a in shlex.split(match.group(1)) if not a.startswith("-")]
            except ValueError:
                args = []
            if len(args) >= 2:
                targets.append(args[-1])
    if heredoc >= 0 or "python" in command:
        body = command if heredoc < 0 else command[heredoc:]
        if _PY_WRITE.search(body):
            targets += _QUOTED_FILE.findall(body)
    clean = []
    for target in targets:
        target = target.strip("\"'")
        # Ziele mit Shell-Variablen ($S/…) sind hier nicht auflösbar; lieber auslassen als falsch blocken
        if not target or target.startswith(("/dev/", "&", "-")) or "://" in target or "$" in target or target in clean:
            continue
        clean.append(target)
    return clean


def actions(data):
    """Was die Aktion tut: Liste von (aktion, ziel). Ziel ist ein absoluter Pfad oder ''."""
    tool = data.get("tool_name") or ""
    tin = data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    result = []
    if tool in FILE_TOOLS:
        path = tin.get("file_path") or tin.get("notebook_path") or ""
        if path:
            result.append(("datei", os.path.normpath(os.path.join(cwd, os.path.expanduser(path)))))
    elif tool == "Bash":
        command = tin.get("command") or ""
        if _GIT_COMMIT.search(command):
            result.append(("bash:commit", ""))
        for target in bash_targets(command):
            result.append(("bash:schreibt", os.path.normpath(os.path.join(cwd, os.path.expanduser(target)))))
    elif _CLICKUP_WRITE.match(tool):
        result.append(("mcp:clickup-schreibt", ""))
    return result


def _match(path, patterns):
    return any(fnmatch.fnmatch(path, p.replace("**", "*")) for p in patterns)


def violations(rules, acts, project, skills, mode):
    """Regeln im gegebenen modus, deren Pflicht-Skill fehlt: Liste von (regel, ziel)."""
    out = []
    always_except = rules.get("ausser_immer", [])
    for rule in rules.get("regeln", []):
        if rule.get("modus") != mode:
            continue
        if rule.get("projekt", "*") not in ("*", project):
            continue
        if any(p in skills for p in rule.get("pflicht", [])):
            continue
        for act, target in acts:
            if act not in rule.get("aktion", []):
                continue
            if rule.get("pfad"):
                if not target or not _match(target, rule["pfad"]):
                    continue
                if _match(target, always_except) or _match(target, rule.get("ausser", [])):
                    continue
            out.append((rule, target))
            break
    return out


def log(entries, data, project):
    if not entries:
        return
    directory = os.environ.get("SKILL_LOG_DIR") or os.path.join(os.path.expanduser("~"), ".claude", "skill-log")
    now = datetime.datetime.now(datetime.timezone.utc)
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, now.strftime("%Y-%m") + ".jsonl"), "a", encoding="utf-8") as fh:
        for entry in entries:
            fh.write(json.dumps(dict({
                "v": 1, "ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "host": os.environ.get("SKILL_LOG_HOST") or socket.gethostname(),
                "session": data.get("session_id"), "event": "guard", "project": project,
                "tool": data.get("tool_name"), "tool_use_id": data.get("tool_use_id"),
            }, **entry), ensure_ascii=False) + "\n")


def message(found):
    lines = []
    for rule, target in found:
        where = f" ({target})" if target else ""
        lines.append(f"- Regel „{rule['id']}“{where}: {rule.get('beschreibung', '')}. "
                     f"Zuständig: {', '.join(rule['pflicht'])}")
    return "\n".join(lines)


def decide(data, rules=None, skills=None):
    """Gibt (exit_code, stdout, stderr, log_entries) zurück. Reine Funktion für Tests."""
    rules = rules if rules is not None else load_rules()
    event = data.get("hook_event_name")
    mode = {"PreToolUse": "blocken", "PostToolUse": "warnen"}.get(event)
    acts = actions(data)
    if not mode or not acts:
        return 0, "", "", []
    project = project_of(data.get("cwd"))
    skills = skills if skills is not None else loaded_skills(transcripts(data))
    found = violations(rules, acts, project, skills, mode)
    if not found:
        return 0, "", "", []
    entries = [{"regel": r["id"], "entscheidung": "geblockt" if mode == "blocken" else "gewarnt",
                "ziel": t[-200:], "pflicht": r["pflicht"], "aktiv": sorted(skills)} for r, t in found]
    text = message(found)
    if mode == "blocken":
        err = ("Skill-Wächter: Diese Änderung braucht einen geladenen Skill, der dafür zuständig ist.\n" + text +
               "\nLade den passenden Skill mit dem Skill-Werkzeug und wiederhole dann die Aktion. "
               "Ist die Regel hier falsch, sag es dem Nutzer (wird bei der Skill-Auswertung nachgeschärft).")
        return 2, "", err, entries
    ctx = ("Skill-Wächter (Hinweis): Diese Aktion lief ohne den zuständigen Skill.\n" + text +
           "\nLade den passenden Skill, bevor du weitermachst, damit sein Ablauf (Profil, Tests, Commit) gilt.")
    out = json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": ctx}},
                     ensure_ascii=False)
    return 0, out, "", entries


def main():
    if (os.environ.get("SKILL_GUARD") or "").lower() in ("aus", "off", "0"):
        return 0
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        code, out, err, entries = decide(data)
        try:
            log(entries, data, project_of(data.get("cwd")))
        except Exception as exc:  # noqa: BLE001 – das Protokoll darf die Entscheidung nicht verhindern
            sys.stderr.write(f"skill_guard log: {exc}\n") if code == 0 else None
        if out:
            sys.stdout.write(out)
        if err:
            sys.stderr.write(err)
        return code
    except Exception:  # noqa: BLE001 – ein Fehler im Wächter darf nie blockieren
        return 0


if __name__ == "__main__":
    sys.exit(main())
