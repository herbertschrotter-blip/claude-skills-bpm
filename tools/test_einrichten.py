#!/usr/bin/env python3
"""Tests für einrichten.py (nur die reinen Funktionen): python3 -m unittest tools/test_einrichten.py"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import einrichten as e  # noqa: E402

MARKET = {"plugins": [
    {"name": "work", "skills": ["./skills/code-erstellen", "./skills/tracker/"]},
    {"name": "skill-workshop", "skills": ["./skills/skill-pflege"]},
    {"name": "work-hooks", "source": "./plugins/work-hooks"},
]}


class EinrichtenTest(unittest.TestCase):
    def test_auto_update_neu(self):
        s = e.with_auto_update({})
        self.assertEqual(s["extraKnownMarketplaces"]["workbench"],
                         {"source": {"source": "github", "repo": e.REPO}, "autoUpdate": True})

    def test_auto_update_behaelt_quelle_und_anderes(self):
        s = e.with_auto_update({"theme": "dark", "extraKnownMarketplaces": {"workbench": {"source": {"source": "x"}}}})
        self.assertEqual(s["theme"], "dark")
        self.assertEqual(s["extraKnownMarketplaces"]["workbench"]["source"], {"source": "x"})
        self.assertTrue(s["extraKnownMarketplaces"]["workbench"]["autoUpdate"])

    def test_overrides_ergaenzt_ohne_vorhandene_zu_aendern(self):
        s = e.with_overrides({"skillOverrides": {"anthropic-skills:tracker": "name-only"}}, ["tracker", "audit"])
        self.assertEqual(s["skillOverrides"], {"anthropic-skills:tracker": "name-only", "anthropic-skills:audit": "off"})

    def test_skills_der_plugins(self):
        self.assertEqual(e.skills_of(MARKET, ["work", "skill-workshop"]), ["code-erstellen", "tracker", "skill-pflege"])

    def test_plan_terminal_ersetzt_work_hooks(self):
        self.assertEqual(e.plan("terminal", {"work-hooks": {}, "work": {}}), (["skill-workshop"], ["work"], ["work-hooks"]))

    def test_plan_desktop_ersetzt_work(self):
        self.assertEqual(e.plan("desktop", {"work": {}, "skill-workshop": {}}),
                         (["work-hooks"], [], ["work", "skill-workshop"]))


if __name__ == "__main__":
    unittest.main()
