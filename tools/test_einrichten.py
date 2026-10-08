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



class SettingsTest(unittest.TestCase):
    def test_leer_ist_leeres_objekt(self):
        self.assertEqual(e.parse_settings("  "), ({}, None))

    def test_kaputt_liefert_lesbaren_fehler(self):
        data, fehler = e.parse_settings('{"a": 1,}')
        self.assertIsNone(data)
        self.assertIn("Zeile 1", fehler)

    def test_kein_objekt(self):
        self.assertEqual(e.parse_settings("[1, 2]"), (None, "kein JSON-Objekt"))

    def test_gueltig(self):
        self.assertEqual(e.parse_settings('{"theme": "dark"}'), ({"theme": "dark"}, None))


class ProtokollTest(unittest.TestCase):
    def test_erster_befund_bleibt(self):
        p = e.merge_protokoll({}, [{"was": "git", "wert": "Git.Git", "aktion": "war-da"}], "t1")
        p = e.merge_protokoll(p, [{"was": "git", "wert": "Git.Git", "aktion": "installiert"}], "t2")
        self.assertEqual(p["eintraege"][0]["aktion"], "war-da")

    def test_entfernt_ersetzt_und_danach_neu(self):
        p = e.merge_protokoll({}, [{"was": "plugin", "wert": "work", "aktion": "installiert"}])
        p = e.merge_protokoll(p, [{"was": "plugin", "wert": "work", "aktion": "entfernt"}])
        self.assertEqual(e.offen(p), [])
        p = e.merge_protokoll(p, [{"was": "plugin", "wert": "work", "aktion": "installiert"}])
        self.assertEqual([x["wert"] for x in e.offen(p, "plugin")], ["work"])

    def test_settings_entfernen_nur_eigene(self):
        s = {"theme": "dark",
             "extraKnownMarketplaces": {"workbench": {"source": {"source": "github"}, "autoUpdate": True}},
             "skillOverrides": {"anthropic-skills:audit": "off", "anthropic-skills:tracker": "name-only",
                                "anthropic-skills:x": "off"}}
        e.settings_entfernen(s, [{"was": "einstellung-autoupdate", "wert": "workbench", "neu_eintrag": False},
                                 {"was": "einstellung-override", "wert": "anthropic-skills:audit"},
                                 {"was": "einstellung-override", "wert": "anthropic-skills:tracker"}])
        self.assertEqual(s["extraKnownMarketplaces"]["workbench"], {"source": {"source": "github"}})
        self.assertEqual(s["skillOverrides"], {"anthropic-skills:tracker": "name-only", "anthropic-skills:x": "off"})
        self.assertEqual(s["theme"], "dark")

    def test_settings_entfernen_neuer_eintrag_ganz(self):
        s = {"extraKnownMarketplaces": {"workbench": {"autoUpdate": True}}}
        e.settings_entfernen(s, [{"was": "einstellung-autoupdate", "wert": "workbench", "neu_eintrag": True}])
        self.assertEqual(s, {})

if __name__ == "__main__":
    unittest.main()
