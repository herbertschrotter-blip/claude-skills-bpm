#!/usr/bin/env python3
"""Skill-Log v1: schreibt Hook-Ereignisse von Claude Code als JSONL (Spezifikation: docs/skill-log-v1.md).

Aufruf als Hook für SessionStart, UserPromptSubmit, PostToolUse (Matcher Skill) und Stop. Liest die Hook-Daten von
stdin und hängt eine Zeile an <SKILL_LOG_DIR>/<JJJJ-MM>.jsonl an. Scheitert nie laut: jeder Fehler endet mit Exit 0,
damit der Chat nie blockiert wird.

Umgebungsvariablen (optional):
  SKILL_LOG_HOST  Name des Rechners im Log (Standard: Hostname)
  SKILL_LOG_DIR   Ablage (Standard: ~/.claude/skill-log)
  SKILL_LOG_RAW   "1" = zusätzlich die rohen Hook-Daten nach raw-<JJJJ-MM>.jsonl schreiben (nur zur Fehlersuche)
"""

import datetime
import json
import os
import re
import socket
import sys

VERSION = 1
PROMPT_MAX = 2000
ARGS_MAX = 300

EVENTS = {
    "SessionStart": "session",
    "UserPromptSubmit": "prompt",
    "PostToolUse": "skill",
    "Stop": "turn_end",
}

# Werte nach typischen Schlüsselwörtern, dazu lange Token-artige Zeichenfolgen (GitHub, JWT, Anthropic, generisch)
_MASK_KEYED = re.compile(
    r"(?i)((?:token|passwor[dt]|passwd|secret|api[_-]?key|access[_-]?key|bearer|authorization|schl(?:ü|ue)ssel)"
    r"\s*[:=]?\s*[\"']?)([^\s\"',;]{6,})"
)
_MASK_BARE = re.compile(
    r"\b(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}"
    r"|eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}"
    r"|[A-Z0-9]{4}(?:-[A-Z0-9]{4}){5,})\b"
)
_SLASH = re.compile(r"^\s*/([A-Za-z0-9][\w:.-]*)")
_PROJECT_ID = re.compile(r"^\s*-\s*Projekt-ID:\s*(\S+)", re.M)


def mask(text):
    text = _MASK_BARE.sub("<MASKIERT>", text)
    return _MASK_KEYED.sub(lambda m: m.group(1) + "<MASKIERT>", text)


def clip(text, limit):
    text = mask(str(text))
    return text if len(text) <= limit else text[:limit] + "…"


def project_of(cwd):
    """Projekt-ID aus dem Skill-Profil der nächsten CLAUDE.md nach oben, sonst der Ordnername."""
    path = os.path.abspath(cwd or os.getcwd())
    probe = path
    while True:
        claude_md = os.path.join(probe, "CLAUDE.md")
        if os.path.isfile(claude_md):
            try:
                with open(claude_md, encoding="utf-8") as fh:
                    found = _PROJECT_ID.search(fh.read())
                if found:
                    return found.group(1)
            except OSError:
                pass
        parent = os.path.dirname(probe)
        if parent == probe:
            return os.path.basename(path) or path
        probe = parent


def skill_fields(data):
    tool_input = data.get("tool_input") or {}
    name = tool_input.get("skill") or tool_input.get("command") or tool_input.get("name")
    response = data.get("tool_response")
    ok = True
    if isinstance(response, dict):
        if response.get("success") is False or response.get("is_error") or response.get("error"):
            ok = False
    args = tool_input.get("args")
    return {"skill": name, "args": clip(args, ARGS_MAX) if args else None, "ok": ok}


def build(data):
    hook = data.get("hook_event_name", "")
    event = EVENTS.get(hook)
    if event is None:
        return None
    if event == "skill" and data.get("tool_name") != "Skill":
        return None
    cwd = data.get("cwd") or os.getcwd()
    entry = {
        "v": VERSION,
        "ts": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "host": os.environ.get("SKILL_LOG_HOST") or socket.gethostname(),
        "session": data.get("session_id"),
        "event": event,
        "project": project_of(cwd),
    }
    if event == "session":
        entry.update({"cwd": cwd, "source": data.get("source")})
    elif event == "prompt":
        prompt = data.get("prompt") or ""
        slash = _SLASH.match(prompt)
        entry.update({"text": clip(prompt, PROMPT_MAX), "slash": slash.group(1) if slash else None})
    elif event == "skill":
        entry.update(skill_fields(data))
    return entry


def append(directory, name, obj):
    os.makedirs(directory, exist_ok=True)
    with open(os.path.join(directory, name), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main():
    try:
        raw = sys.stdin.read()
        data = json.loads(raw) if raw.strip() else {}
        directory = os.environ.get("SKILL_LOG_DIR") or os.path.join(os.path.expanduser("~"), ".claude", "skill-log")
        month = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m")
        if os.environ.get("SKILL_LOG_RAW") == "1":
            append(directory, f"raw-{month}.jsonl", data)
        entry = build(data)
        if entry:
            append(directory, f"{month}.jsonl", entry)
    except Exception as exc:  # noqa: BLE001 – ein Protokoll darf den Chat nie stören
        sys.stderr.write(f"skill_log: {exc}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
