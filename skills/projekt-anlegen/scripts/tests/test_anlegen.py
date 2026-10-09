"""Tests für den Ablauf Prepare → Verify → Publish (generate.anlegen) mit einem kleinen Testkatalog ohne Netz."""

import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import generate as g  # noqa: E402
import pruefung as p  # noqa: E402
from test_bausteine import katalog_ordner  # noqa: E402

KATALOG = {
    "basis": {"id": "basis", "requires": [], "files": [{"source": "basis/README.md.tpl", "target": "README.md"}]},
    "kern": {"id": "kern", "requires": ["basis"],
             "files": [{"source": "kern/main.py.tpl", "target": "{{package}}/__main__.py"}]},
}
INHALTE = {"basis/README.md.tpl": "# {{name}}\n", "kern/main.py.tpl": 'import json\nprint(json.dumps({"status": "ready"}))\n'}


def art(checks):
    return {"id": "werkzeug", "version": 1, "components": ["basis", "kern"], "features": {},
            "kombinationen": [{}], "pruefung": {"einrichten": [], "checks": checks}}


START = {"name": "start", "befehl": ["{python}", "-m", "{package}"], "ausgabe_json": {"status": "ready"}}
AUFTRAG = {
    "schema_version": 1,
    "project": {"name": "Test", "slug": "test-projekt", "package": "testprojekt"},
    "template": {"id": "werkzeug", "version": 1},
    "features": {},
    "delivery": {"github": False},
}


class AnlegenTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp, True)
        self.ablage = self.tmp / "ablage"
        self.ablage.mkdir()

    def katalog(self, checks):
        return katalog_ordner(self.tmp / "katalog", katalog=KATALOG, art=art(checks), inhalte=INHALTE)

    def test_gruen_wird_veroeffentlicht(self):
        r = g.anlegen(AUFTRAG, self.ablage, self.katalog([START]))
        self.assertTrue(r["ok"], r)
        self.assertEqual([x["name"] for x in r["pruefungen"]], ["einrichten", "start"])
        self.assertEqual(sorted(os.listdir(self.ablage)), ["test-projekt"])
        self.assertTrue((self.ablage / "test-projekt" / "testprojekt" / "__main__.py").is_file())
        self.assertTrue((self.ablage / "test-projekt" / g.HERKUNFT).is_file())

    def test_roter_check_legt_nichts_an(self):
        rot = {"name": "tests", "befehl": ["{python}", "-c", "import sys; print('kaputt'); sys.exit(3)"]}
        r = g.anlegen(AUFTRAG, self.ablage, self.katalog([START, rot]))
        self.assertFalse(r["ok"])
        self.assertEqual(r["phase"], "pruefen")
        self.assertIn("tests fehlgeschlagen", r["fehler"][0])
        self.assertIn("kaputt", r["pruefungen"][-1]["ausgabe"])
        self.assertEqual(os.listdir(self.ablage), [])  # auch kein Zwischenordner

    def test_falsche_ausgabe(self):
        falsch = dict(START, ausgabe_json={"status": "anders"})
        r = g.anlegen(AUFTRAG, self.ablage, self.katalog([falsch]))
        self.assertFalse(r["ok"])
        self.assertIn("erwartet", r["pruefungen"][-1]["ausgabe"])
        self.assertEqual(os.listdir(self.ablage), [])

    def test_check_sieht_tmp_und_umgebung(self):
        check = {"name": "env", "umgebung": {"{package_upper}_DATEN": "{tmp}"},
                 "befehl": ["{python}", "-c", "import os,sys; sys.exit(0 if os.path.isdir(os.environ['TESTPROJEKT_DATEN']) else 1)"]}
        self.assertTrue(g.anlegen(AUFTRAG, self.ablage, self.katalog([check]))["ok"])

    def test_ziel_existiert(self):
        (self.ablage / "test-projekt").mkdir()
        r = g.anlegen(AUFTRAG, self.ablage, self.katalog([START]))
        self.assertFalse(r["ok"])
        self.assertEqual(r["phase"], "auftrag")
        self.assertEqual(os.listdir(self.ablage), ["test-projekt"])

    def test_ungueltiger_auftrag(self):
        r = g.anlegen(dict(AUFTRAG, befehl="x"), self.ablage, self.katalog([START]))
        self.assertFalse(r["ok"])
        self.assertIn("befehl: unbekanntes Feld", r["fehler"])
        self.assertEqual(os.listdir(self.ablage), [])

    def test_unbekannter_platzhalter_im_pruefbefehl(self):
        self.assertTrue(p.tokens_pruefen({"checks": [{"name": "x", "befehl": ["{owner}"]}]}))
        self.assertEqual(p.tokens_pruefen({"checks": [START]}), [])

    def test_befehlszeile(self):
        katalog = self.katalog([START])
        auftrag = self.tmp / "auftrag.json"
        auftrag.write_text(json.dumps(AUFTRAG), encoding="utf-8")
        alt = g.TEMPLATES
        g.anlegen.__defaults__ = (katalog, True)
        try:
            with contextlib.redirect_stdout(io.StringIO()) as out:
                self.assertEqual(g.main(["--auftrag", str(auftrag), "--ablage", str(self.ablage)]), 0)
                self.assertEqual(g.main(["--auftrag", str(auftrag), "--ablage", str(self.ablage)]), 1)  # existiert
            self.assertIn('"ok": true', out.getvalue())
        finally:
            g.anlegen.__defaults__ = (alt, True)


if __name__ == "__main__":
    unittest.main()
