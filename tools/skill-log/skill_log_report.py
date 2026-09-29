#!/usr/bin/env python3
"""Auswertung des Skill-Logs v1 (Spezifikation: docs/skill-log-v1.md).

Liest alle <JJJJ-MM>.jsonl aus einem oder mehreren Ordnern (z. B. HA und Laptop), bildet Runden (Prompt bis turn_end)
und zeigt je Skill, wie oft er gezündet hat, dazu Prompts ohne Skill und Runden mit mehreren Skills.

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


def build_rounds(entries):
    """Eine Runde = ein Prompt mit allen Skill-Aufrufen bis zum nächsten Prompt oder turn_end derselben Sitzung."""
    rounds = []
    open_round = {}
    for entry in entries:
        session = (entry.get("host"), entry.get("session"))
        event = entry.get("event")
        if event == "prompt":
            current = {
                "ts": entry.get("ts"),
                "host": entry.get("host"),
                "session": entry.get("session"),
                "project": entry.get("project"),
                "text": entry.get("text") or "",
                "slash": entry.get("slash"),
                "skills": [],
            }
            rounds.append(current)
            open_round[session] = current
        elif event == "skill" and session in open_round:
            open_round[session]["skills"].append({"skill": entry.get("skill"), "ok": entry.get("ok", True)})
        elif event == "turn_end":
            open_round.pop(session, None)
    return rounds


def short(name):
    return (name or "?").split(":")[-1]


def report(rounds, limit_without):
    total = len(rounds)
    with_skill = [r for r in rounds if r["skills"]]
    without = [r for r in rounds if not r["skills"]]
    multi = [r for r in rounds if len(r["skills"]) > 1]

    auto = collections.Counter()
    manual = collections.Counter()
    failed = collections.Counter()
    for r in rounds:
        for s in r["skills"]:
            name = short(s["skill"])
            if r["slash"] and short(r["slash"]) == name:
                manual[name] += 1
            else:
                auto[name] += 1
            if not s["ok"]:
                failed[name] += 1

    print(f"Runden: {total}  mit Skill: {len(with_skill)}  ohne Skill: {len(without)}  mehrere Skills: {len(multi)}")
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
            print(f"  {r['ts']} [{r['project']}] {names}: {r['text'][:100]!r}")

    if without:
        shown = without[-limit_without:] if limit_without else without
        print(f"\nPrompts ohne Skill (letzte {len(shown)} von {len(without)}) – hätte einer zünden müssen?")
        for r in shown:
            print(f"  {r['ts']} [{r['project']}] {r['text'][:120]!r}")


def main():
    parser = argparse.ArgumentParser(description="Auswertung Skill-Log v1")
    parser.add_argument("dirs", nargs="*", default=["~/.claude/skill-log"], help="Log-Ordner (mehrere möglich)")
    parser.add_argument("--since", help="ab Datum JJJJ-MM-TT (UTC)")
    parser.add_argument("--host", help="nur dieser Rechner")
    parser.add_argument("--project", help="nur diese Projekt-ID")
    parser.add_argument("--ohne-skill", type=int, default=30, help="so viele Prompts ohne Skill zeigen (0 = alle)")
    parser.add_argument("--json", action="store_true", help="Runden als JSON ausgeben statt Bericht")
    args = parser.parse_args()

    rounds = build_rounds(read_entries(args.dirs))
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
