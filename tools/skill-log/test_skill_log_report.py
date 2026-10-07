#!/usr/bin/env python3
"""Tests für skill_log_report.py (nur Standardbibliothek): python3 -m unittest tools/skill-log/test_skill_log_report.py"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_log_report as r  # noqa: E402

SKILLS = {"projekt-anlegen", "mockup-erstellen", "ticket", "code-erstellen", "tracker"}


def e(ts, event, session="s1", **kw):
    return dict({"v": 1, "ts": f"2026-10-01T10:{ts:02d}:00Z", "host": "h", "session": session, "event": event,
                 "project": "p"}, **kw)


class SlashTest(unittest.TestCase):
    def test_slash_skill_zaehlt_per_name(self):
        rounds = r.build_rounds([e(1, "prompt", text="/projekt-anlegen", slash="projekt-anlegen"),
                                 e(2, "skill", skill="anthropic-skills:mockup-erstellen"), e(3, "turn_end")], SKILLS)
        self.assertEqual([(s["skill"], s["via"]) for s in rounds[0]["skills"]],
                         [("projekt-anlegen", "slash"), ("anthropic-skills:mockup-erstellen", "tool")])

    def test_slash_ohne_skill_bleibt_ohne_skill(self):
        rounds = r.build_rounds([e(1, "prompt", text="/clear", slash="clear"), e(2, "turn_end")], SKILLS)
        self.assertEqual(rounds[0]["skills"], [])

    def test_slash_und_skill_ereignis_nicht_doppelt(self):
        rounds = r.build_rounds([e(1, "prompt", text="/ticket", slash="ticket"),
                                 e(2, "skill", skill="anthropic-skills:ticket"), e(3, "turn_end")], SKILLS)
        self.assertEqual(len(rounds[0]["skills"]), 1)


class ArtTest(unittest.TestCase):
    def test_systemmeldungen_und_leere_prompts(self):
        self.assertEqual(r.prompt_kind("<task-notification> <task-id>x</task-id>"), "system")
        self.assertEqual(r.prompt_kind("  <agent-message from='a'>"), "system")
        self.assertEqual(r.prompt_kind("   "), "leer")
        self.assertEqual(r.prompt_kind("nächstes ticket"), "prompt")


class AktivTest(unittest.TestCase):
    def test_skill_bleibt_in_der_sitzung_aktiv(self):
        rounds = r.build_rounds([e(1, "prompt", text="tickets prüfen"), e(2, "skill", skill="anthropic-skills:ticket"),
                                 e(3, "turn_end"), e(4, "prompt", text="nächstes ticket"), e(5, "turn_end")], SKILLS)
        self.assertEqual(rounds[0]["aktiv"], [])
        self.assertEqual(rounds[1]["aktiv"], ["ticket"])

    def test_gabelung_erbt_skills_aus_dem_transcript(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "-config-projekte-x"))
            lines = [
                {"timestamp": "2026-10-01T09:00:00.000Z", "type": "assistant", "message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "anthropic-skills:ticket"}}]}},
                {"timestamp": "2026-10-01T09:01:00.000Z", "type": "user",
                 "message": {"content": "<command-name>/anthropic-skills:mockup-erstellen</command-name>"}},
                {"timestamp": "2026-10-01T11:00:00.000Z", "type": "assistant", "message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "tracker"}}]}},
            ]
            with open(os.path.join(tmp, "-config-projekte-x", "fork1.jsonl"), "w", encoding="utf-8") as fh:
                fh.write("\n".join(json.dumps(x) for x in lines))
            rounds = r.build_rounds([e(0, "session", session="fork1", source="fork", cwd="/config/projekte/x"),
                                     e(1, "prompt", session="fork1", text="nächstes ticket"),
                                     e(2, "turn_end", session="fork1")], SKILLS, transcripts_dir=tmp)
        self.assertEqual(rounds[0]["aktiv"], ["mockup-erstellen", "ticket"])

    def test_skills_nach_compaction_und_fremde_skills_zaehlen(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, "-config"))
            lines = [
                {"timestamp": "2026-10-01T09:00:00.000Z", "type": "attachment", "attachment": {
                    "type": "invoked_skills", "skills": [{"name": "anthropic-skills:mockup-erstellen"}]}},
                {"timestamp": "2026-10-01T09:01:00.000Z", "type": "assistant", "message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "update-config"}}]}},
                {"timestamp": "2026-10-01T09:02:00.000Z", "type": "user",
                 "message": {"content": "<command-name>/clear</command-name>"}},
            ]
            with open(os.path.join(tmp, "-config", "c1.jsonl"), "w", encoding="utf-8") as fh:
                fh.write("\n".join(json.dumps(x) for x in lines))
            rounds = r.build_rounds([e(1, "prompt", session="c1", text="weiter"), e(2, "turn_end", session="c1")],
                                    SKILLS, transcripts_dir=tmp)
        self.assertEqual(rounds[0]["aktiv"], ["mockup-erstellen", "update-config"])

    def test_ohne_transcript_nichts_aktiv(self):
        rounds = r.build_rounds([e(1, "prompt", text="x"), e(2, "turn_end")], SKILLS, transcripts_dir="/gibt/es/nicht")
        self.assertEqual(rounds[0]["aktiv"], [])


class UnsicherTest(unittest.TestCase):
    def test_prompt_vor_turn_end_ist_unsicher(self):
        rounds = r.build_rounds([e(1, "prompt", text="mach mit agenten"), e(2, "prompt", text="frage nebenbei"),
                                 e(3, "skill", skill="workflow-authoring"), e(4, "turn_end")], SKILLS | {"workflow-authoring"})
        self.assertFalse(rounds[0]["unsicher"])
        self.assertTrue(rounds[1]["unsicher"])

    def test_normaler_ablauf_ist_sicher(self):
        rounds = r.build_rounds([e(1, "prompt", text="a"), e(2, "turn_end"), e(3, "prompt", text="b"),
                                 e(4, "turn_end")], SKILLS)
        self.assertFalse(rounds[1]["unsicher"])


class GuardTest(unittest.TestCase):
    def test_waechter_ereignis_haengt_an_der_runde(self):
        rounds = r.build_rounds([e(1, "prompt", text="weiter"),
                                 e(2, "guard", regel="code", entscheidung="geblockt", ziel="/x/a.py", tool="Edit"),
                                 e(3, "skill", skill="code-erstellen"), e(4, "turn_end")], SKILLS)
        self.assertEqual(rounds[0]["guard"][0]["regel"], "code")
        self.assertEqual(rounds[0]["skills"][0]["skill"], "code-erstellen")


if __name__ == "__main__":
    unittest.main()
