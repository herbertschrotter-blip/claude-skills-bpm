#!/usr/bin/env python3
"""Tests für skill_guard.py (nur Standardbibliothek): python3 -m unittest plugins/work-hooks/hooks/test_skill_guard.py"""

import copy
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_guard as g  # noqa: E402

RULES = g.load_rules(os.path.join(os.path.dirname(os.path.abspath(__file__)), "regeln.json"))
# Die Mechanik wird gegen feste Modi geprüft; die echten Modi ändern sich beim Lernen (skill-auswertung)
MECH = copy.deepcopy(RULES)
for _rule in MECH["regeln"]:
    _rule["modus"] = "blocken" if _rule["id"] in ("code", "mockup") else "warnen"


def hook(event, tool, tool_input, cwd="/home/nutzer/projekte/demo"):
    return {"hook_event_name": event, "tool_name": tool, "tool_input": tool_input, "cwd": cwd,
            "session_id": "s1", "tool_use_id": "t1"}


class RegelnTest(unittest.TestCase):
    def test_regeldatei_ist_gueltig(self):
        ids = [r["id"] for r in RULES["regeln"]]
        self.assertEqual(len(ids), len(set(ids)))
        for rule in RULES["regeln"]:
            self.assertIn(rule["modus"], ("blocken", "warnen", "aus"))
            self.assertTrue(rule["pflicht"])
            self.assertTrue(set(rule["aktion"]) <= {"datei", "bash:schreibt", "bash:commit", "mcp:clickup-schreibt"})


class BlockenTest(unittest.TestCase):
    def test_code_ohne_code_erstellen_wird_geblockt(self):
        code, _, err, entries = g.decide(hook("PreToolUse", "Edit", {"file_path": "logik/rechte.py"}), MECH, set())
        self.assertEqual(code, 2)
        self.assertIn("code-erstellen", err)
        self.assertEqual(entries[0]["regel"], "code")

    def test_code_mit_code_erstellen_laeuft(self):
        code, _, _, _ = g.decide(hook("PreToolUse", "Edit", {"file_path": "logik/rechte.py"}), MECH,
                                 {"code-erstellen", "tracker"})
        self.assertEqual(code, 0)

    def test_ticket_reicht_fuer_code(self):
        code, _, _, _ = g.decide(hook("PreToolUse", "Write", {"file_path": "x.js"}), MECH, {"ticket"})
        self.assertEqual(code, 0)

    def test_mockup_braucht_mockup_erstellen(self):
        data = hook("PreToolUse", "Write", {"file_path": "/home/nutzer/projekte/demo/mockups/quelle/symbol.js"})
        code, _, err, _ = g.decide(data, MECH, {"code-erstellen"})
        self.assertEqual(code, 2)
        self.assertIn("mockup-erstellen", err)
        self.assertEqual(g.decide(data, MECH, {"mockup-erstellen"})[0], 0)

    def test_shell_schreiben_wird_erkannt(self):
        data = hook("PreToolUse", "Bash", {"command": "cat > custom_components/baustelle/logik/rechte.py <<'EOF'\nx=1\nEOF"})
        self.assertEqual(g.decide(data, MECH, set())[0], 2)

    def test_shell_lesen_bleibt_frei(self):
        data = hook("PreToolUse", "Bash", {"command": "sed -n 1,40p logik/soll.py; grep -n x panel.py | head"})
        self.assertEqual(g.decide(data, MECH, set())[0], 0)

    def test_ziel_mit_shell_variable_bleibt_frei(self):
        data = hook("PreToolUse", "Bash", {"command": "python3 x.py > $S/runden.json; cat > $S/tx.py <<'E'\nE"})
        self.assertEqual(g.decide(data, MECH, set())[0], 0)

    def test_scratchpad_und_tmp_sind_frei(self):
        for path in ("/tmp/claude-0/x/scratchpad/a.py", "/tmp/x.json", "/home/nutzer/.claude/skill-log/a.json"):
            self.assertEqual(g.decide(hook("PreToolUse", "Write", {"file_path": path}), MECH, set())[0], 0, path)

    def test_warnregeln_blocken_nicht(self):
        code, _, _, _ = g.decide(hook("PreToolUse", "Edit", {"file_path": "docs/bauplan.md"}), MECH, set())
        self.assertEqual(code, 0)


class WarnenTest(unittest.TestCase):
    def test_doku_ohne_skill_gibt_hinweis_nach_der_aktion(self):
        code, out, _, entries = g.decide(hook("PostToolUse", "Edit", {"file_path": "docs/bauplan.md"}), MECH, set())
        self.assertEqual(code, 0)
        ctx = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(ctx["hookEventName"], "PostToolUse")
        self.assertIn("doc-pflege", ctx["additionalContext"])
        self.assertEqual(entries[0]["entscheidung"], "gewarnt")

    def test_clickup_ohne_tracker_warnt(self):
        data = hook("PostToolUse", "mcp__claude_ai_ClickUp__clickup_create_task", {"name": "x"})
        self.assertIn("tracker", g.decide(data, MECH, set())[1])
        self.assertEqual(g.decide(data, MECH, {"tracker"})[1], "")

    def test_clickup_lesen_ist_frei(self):
        data = hook("PostToolUse", "mcp__claude_ai_ClickUp__clickup_filter_tasks", {})
        self.assertEqual(g.decide(data, MECH, set())[1], "")

    def test_commit_ohne_skill_warnt(self):
        data = hook("PostToolUse", "Bash", {"command": "git add x && git commit -q -m 'x'"})
        self.assertIn("commit", g.decide(data, MECH, set())[1])

    def test_blockregel_warnt_nicht_nochmal(self):
        data = hook("PostToolUse", "Edit", {"file_path": "logik/rechte.py"})
        self.assertEqual(g.decide(data, MECH, set())[1], "")


class ProjektTest(unittest.TestCase):
    def test_skills_regel_nur_im_skill_repo(self):
        repo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
        data = hook("PostToolUse", "Edit", {"file_path": "skills/tracker/SKILL.md"}, cwd=os.path.abspath(repo))
        self.assertIn("skill-pflege", g.decide(data, MECH, set())[1])
        data = hook("PostToolUse", "Edit", {"file_path": "/anderswo/skills/x/SKILL.md"}, cwd="/anderswo")
        self.assertNotIn("skill-pflege", g.decide(data, MECH, set())[1])


class TranscriptTest(unittest.TestCase):
    def test_skills_aus_haupt_und_subagent_transcript(self):
        with tempfile.TemporaryDirectory() as tmp:
            main = os.path.join(tmp, "s1.jsonl")
            sub = os.path.join(tmp, "s1", "subagents", "agent-a.jsonl")
            os.makedirs(os.path.dirname(sub))
            with open(main, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "anthropic-skills:code-erstellen"}}]}}) + "\n")
                fh.write(json.dumps({"message": {"content": "<command-name>/mockup-erstellen</command-name>"}}) + "\n")
            with open(sub, "w", encoding="utf-8") as fh:
                fh.write("{}\n")
            paths = g.transcripts({"transcript_path": sub, "session_id": "s1"})
            self.assertIn(main, paths)
            self.assertEqual(g.loaded_skills(paths), {"code-erstellen", "mockup-erstellen"})

    def test_skills_nach_compaction_aus_anhang(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s2.jsonl")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"type": "attachment", "attachment": {"type": "invoked_skills", "skills": [
                    {"name": "anthropic-skills:code-erstellen", "content": "…"}, {"name": "update-config"}]}}) + "\n")
            self.assertEqual(g.loaded_skills([path]), {"code-erstellen", "update-config"})


class SicherheitTest(unittest.TestCase):
    def test_kaputte_eingabe_blockiert_nie(self):
        self.assertEqual(g.decide({"hook_event_name": "PreToolUse"}, MECH, set())[0], 0)
        self.assertEqual(g.decide({}, MECH, set())[0], 0)


if __name__ == "__main__":
    unittest.main()
