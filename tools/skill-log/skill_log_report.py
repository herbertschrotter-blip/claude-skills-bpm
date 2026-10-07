#!/usr/bin/env python3
"""Auswertung des Skill-Logs v1 (Spezifikation: docs/skill-log-v1.md).

Liest alle <JJJJ-MM>.jsonl aus einem oder mehreren Ordnern (z. B. HA und Laptop), bildet Runden (Prompt bis turn_end)
und zeigt je Skill, wie oft er gezündet hat, dazu Prompts ohne Skill und Runden mit mehreren Skills.

Je Runde führt die Auswertung außerdem:
- `art`: `prompt`, `system` (Meldung einer Hintergrundaufgabe oder eines Subagenten) oder `leer` (nur Bild o. Ä.)
- `aktiv`: Skills, die in der Sitzung vorher schon geladen waren; sie bleiben bis zum Sitzungsende im Kontext. Was eine
  Sitzung vor dem Log geladen hatte (Gabelung mit `fork`, Fortsetzung mit `resume`), kommt aus ihrem Transcript.
- `unsicher`: der Prompt kam, bevor die vorige Runde mit turn_end endete; Skill-Aufrufe können zur vorigen gehören.
Ein Slash-Aufruf eines Skills (`/projekt-anlegen`) zählt als Zündung per /name, auch ohne Skill-Ereignis im Log.

Beispiele:
  python3 skill_log_report.py
  python3 skill_log_report.py --since 2026-09-01 --project ha-config
  python3 skill_log_report.py ~/.claude/skill-log /pfad/zum/laptop-log --ohne-skill 50
  python3 skill_log_report.py --json > runden.json     # Runden als JSON, z. B. als Grundlage für evals/
"""

import argparse
import collections
import glob
import json
import os
import re
import sys

_MONTH_FILE = re.compile(r"^\d{4}-\d{2}\.jsonl$")
_SYSTEM_PREFIXES = ("<task-notification", "<agent-message")
_COMMAND_NAME = re.compile(r"<command-name>/?([\w:.-]+)</command-name>")
_REPO_SKILLS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "skills")


def read_entries(directories):
    entries = []
    for directory in directories:
        for path in sorted(glob.glob(os.path.join(os.path.expanduser(directory), "*.jsonl"))):
            if not _MONTH_FILE.match(os.path.basename(path)):
                continue
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if entry.get("v") == 1:
                        entries.append(entry)
    entries.sort(key=lambda e: (e.get("ts") or ""))
    return entries


def short(name):
    return (name or "?").split(":")[-1]


def prompt_kind(text):
    stripped = (text or "").strip()
    if not stripped:
        return "leer"
    if stripped.startswith(_SYSTEM_PREFIXES):
        return "system"
    return "prompt"


def known_skill_names(entries, skills_dir=_REPO_SKILLS):
    """Namen, die als Skill gelten: alle im Log gezündeten und alle Ordner unter skills/ des Repos."""
    names = {short(e.get("skill")) for e in entries if e.get("event") == "skill"}
    if skills_dir and os.path.isdir(skills_dir):
        names |= {d for d in os.listdir(skills_dir) if os.path.isfile(os.path.join(skills_dir, d, "SKILL.md"))}
    names.discard("?")
    return names


def transcript_path(transcripts_dir, session):
    """Claude Code legt Transcripts unter <projects>/<Ordner je Arbeitsverzeichnis>/<session>.jsonl ab."""
    if not (transcripts_dir and session):
        return None
    matches = glob.glob(os.path.join(os.path.expanduser(transcripts_dir), "*", glob.escape(session) + ".jsonl"))
    return matches[0] if matches else None


def skills_before(path, until_ts):
    """Skills, die laut Transcript vor `until_ts` geladen wurden: (Skill-Aufrufe und Anhang invoked_skills, Slash-Befehle).

    Skill-Aufrufe sind sicher Skills; Slash-Befehle können auch eingebaute Befehle sein (/clear) und werden vom Aufrufer
    gegen die bekannten Skill-Namen gefiltert."""
    found = set()
    tool_skills = set()
    until = (until_ts or "").replace("Z", "")
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if until and (msg.get("timestamp") or "")[:19] >= until[:19]:
                    break
                attachment = msg.get("attachment")
                if isinstance(attachment, dict) and attachment.get("type") == "invoked_skills":
                    tool_skills.update(short(s.get("name")) for s in attachment.get("skills") or [])
                    continue
                content = (msg.get("message") or {}).get("content")
                if isinstance(content, str):
                    found.update(short(m) for m in _COMMAND_NAME.findall(content))
                elif isinstance(content, list):
                    for block in content:
                        if block.get("type") == "tool_use" and block.get("name") == "Skill":
                            tool_skills.add(short((block.get("input") or {}).get("skill")))
                        elif block.get("type") == "text":
                            found.update(short(m) for m in _COMMAND_NAME.findall(block.get("text") or ""))
    except OSError:
        return set(), set()
    found.discard("?")
    tool_skills.discard("?")
    return tool_skills, found


def build_rounds(entries, skill_names=None, transcripts_dir=None):
    """Eine Runde = ein Prompt mit allen Skill-Aufrufen bis zum nächsten Prompt oder turn_end derselben Sitzung."""
    skill_names = known_skill_names(entries) if skill_names is None else skill_names
    rounds = []
    open_round = {}
    active = {}
    seen = set()
    for entry in entries:
        session = (entry.get("host"), entry.get("session"))
        event = entry.get("event")
        if session not in seen:
            seen.add(session)
            path = transcript_path(transcripts_dir, entry.get("session"))
            if path:
                tool_skills, slash = skills_before(path, entry.get("ts"))
                active[session] = tool_skills | (slash & skill_names)
            else:
                active[session] = set()
        if event == "prompt":
            text = entry.get("text") or ""
            slash = entry.get("slash")
            current = {
                "ts": entry.get("ts"),
                "host": entry.get("host"),
                "session": entry.get("session"),
                "project": entry.get("project"),
                "text": text,
                "slash": slash,
                "art": prompt_kind(text),
                "aktiv": sorted(active.get(session, set())),
                "unsicher": session in open_round,
                "skills": [],
                "guard": [],
            }
            if slash and short(slash) in skill_names:
                current["skills"].append({"skill": slash, "ok": True, "via": "slash"})
                active.setdefault(session, set()).add(short(slash))
            rounds.append(current)
            open_round[session] = current
        elif event == "skill":
            name = short(entry.get("skill"))
            active.setdefault(session, set()).add(name)
            if session in open_round:
                skills = open_round[session]["skills"]
                if any(s.get("via") == "slash" and short(s["skill"]) == name for s in skills):
                    continue
                skills.append({"skill": entry.get("skill"), "ok": entry.get("ok", True), "via": "tool"})
        elif event == "guard" and session in open_round:
            open_round[session]["guard"].append({k: entry.get(k) for k in ("regel", "entscheidung", "ziel", "tool")})
        elif event == "turn_end":
            open_round.pop(session, None)
    return rounds


def report(rounds, limit_without):
    prompts = [r for r in rounds if r["art"] == "prompt"]
    system = sum(1 for r in rounds if r["art"] == "system")
    empty = sum(1 for r in rounds if r["art"] == "leer")
    with_skill = [r for r in prompts if r["skills"]]
    without = [r for r in prompts if not r["skills"]]
    without_active = [r for r in without if not r["aktiv"]]
    multi = [r for r in prompts if len(r["skills"]) > 1]
    unsure = [r for r in prompts if r["unsicher"] and r["skills"]]

    auto = collections.Counter()
    manual = collections.Counter()
    failed = collections.Counter()
    for r in rounds:
        for s in r["skills"]:
            name = short(s["skill"])
            if s.get("via") == "slash" or (r["slash"] and short(r["slash"]) == name):
                manual[name] += 1
            else:
                auto[name] += 1
            if not s["ok"]:
                failed[name] += 1

    print(f"Runden: {len(rounds)}  davon Systemmeldungen: {system}  leer: {empty}")
    print(f"Prompts: {len(prompts)}  mit Skill: {len(with_skill)}  ohne Skill: {len(without)} "
          f"(davon ohne aktiven Skill der Sitzung: {len(without_active)})  mehrere Skills: {len(multi)}  "
          f"unsicher zugeordnet: {len(unsure)}")
    if rounds:
        print(f"Zeitraum: {rounds[0]['ts']} bis {rounds[-1]['ts']}")
    print()
    print(f"{'Skill':<24}{'automatisch':>12}{'per /name':>11}{'Fehler':>8}")
    for name in sorted(set(auto) | set(manual), key=lambda n: -(auto[n] + manual[n])):
        print(f"{name:<24}{auto[name]:>12}{manual[name]:>11}{failed[name]:>8}")

    if multi:
        print("\nRunden mit mehreren Skills:")
        for r in multi:
            names = ", ".join(short(s["skill"]) for s in r["skills"])
            flag = " [unsicher]" if r["unsicher"] else ""
            print(f"  {r['ts']} [{r['project']}] {names}{flag}: {r['text'][:100]!r}")

    if unsure:
        print("\nUnsicher zugeordnet (Prompt kam vor dem Ende der vorigen Runde) – Skill gehört evtl. zur vorigen:")
        for r in unsure:
            names = ", ".join(short(s["skill"]) for s in r["skills"])
            print(f"  {r['ts']} [{r['project']}] {names}: {r['text'][:100]!r}")

    guard = collections.Counter((g["regel"], g["entscheidung"]) for r in rounds for g in r.get("guard", []))
    if guard:
        print("\nSkill-Wächter (docs/skill-guard-v1.md) – Treffer je Regel:")
        for rule in sorted({k[0] for k in guard}):
            print(f"  {rule:<12} geblockt: {guard[(rule, 'geblockt')]:>4}  gewarnt: {guard[(rule, 'gewarnt')]:>4}")

    if without:
        shown = without[-limit_without:] if limit_without else without
        print(f"\nPrompts ohne Skill (letzte {len(shown)} von {len(without)}) – hätte einer zünden müssen?")
        print("  [aktiv: …] = in der Sitzung schon geladen, meist kein Fehlausfall")
        for r in shown:
            flag = f" [aktiv: {', '.join(r['aktiv'])}]" if r["aktiv"] else ""
            print(f"  {r['ts']} [{r['project']}]{flag} {r['text'][:120]!r}")


def main():
    parser = argparse.ArgumentParser(description="Auswertung Skill-Log v1")
    parser.add_argument("dirs", nargs="*", default=["~/.claude/skill-log"], help="Log-Ordner (mehrere möglich)")
    parser.add_argument("--since", help="ab Datum JJJJ-MM-TT (UTC)")
    parser.add_argument("--host", help="nur dieser Rechner")
    parser.add_argument("--project", help="nur diese Projekt-ID")
    parser.add_argument("--ohne-skill", type=int, default=30, help="so viele Prompts ohne Skill zeigen (0 = alle)")
    parser.add_argument("--transcripts", default="~/.claude/projects",
                        help="Ordner der Claude-Code-Transcripts für schon geladene Skills ('' = nicht lesen)")
    parser.add_argument("--json", action="store_true", help="Runden als JSON ausgeben statt Bericht")
    args = parser.parse_args()

    entries = read_entries(args.dirs)
    rounds = build_rounds(entries, transcripts_dir=args.transcripts or None)
    if args.since:
        rounds = [r for r in rounds if (r["ts"] or "") >= args.since]
    if args.host:
        rounds = [r for r in rounds if r["host"] == args.host]
    if args.project:
        rounds = [r for r in rounds if r["project"] == args.project]

    if args.json:
        json.dump(rounds, sys.stdout, ensure_ascii=False, indent=1)
        print()
    else:
        report(rounds, args.ohne_skill)
    return 0


if __name__ == "__main__":
    sys.exit(main())
