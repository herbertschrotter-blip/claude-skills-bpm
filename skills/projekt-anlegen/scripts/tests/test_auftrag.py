"""Tests für auftrag.py: python3 -m unittest discover -s skills/projekt-anlegen/scripts/tests"""

import copy
import json
import os
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import auftrag as a  # noqa: E402

KATALOG = {"python-tool": {"id": "python-tool", "version": 1, "features": {"storage": ["none", "sqlite"]}}}
GUT = {
    "schema_version": 1,
    "project": {"name": "Beispiel Werkzeug", "slug": "beispiel-werkzeug", "package": "beispiel_werkzeug"},
    "template": {"id": "python-tool", "version": 1},
    "features": {"storage": "sqlite"},
    "delivery": {"github": False},
}


def mit(**aenderungen):
    """Kopie von GUT; Schlüssel mit Punkt ändern verschachtelte Felder, None entfernt sie."""
    data = copy.deepcopy(GUT)
    for pfad, wert in aenderungen.items():
        teile = pfad.split("__")
        ziel = data
        for teil in teile[:-1]:
            ziel = ziel[teil]
        if wert is None:
            ziel.pop(teile[-1])
        else:
            ziel[teile[-1]] = wert
    return data


class GueltigTest(unittest.TestCase):
    def test_gueltiger_auftrag(self):
        self.assertEqual(a.pruefen(copy.deepcopy(GUT), KATALOG), GUT)

    def test_ohne_speicher_und_mit_github(self):
        a.pruefen(mit(features__storage="none", delivery__github=True), KATALOG)

    def test_mitgelieferter_katalog_kennt_python_tool(self):
        self.assertIn("python-tool", a.manifeste())
        a.pruefen(copy.deepcopy(GUT))


class FehlerTest(unittest.TestCase):
    def fehler(self, data):
        with self.assertRaises(a.AuftragFehler) as ctx:
            a.pruefen(data, KATALOG)
        return " | ".join(ctx.exception.fehler)

    def test_kein_objekt(self):
        self.assertIn("Objekt", self.fehler([1, 2]))

    def test_zusaetzliche_felder_auf_jeder_ebene(self):
        self.assertIn("befehl: unbekanntes Feld", self.fehler(mit(befehl="rm -rf /")))
        self.assertIn("project.pfad: unbekanntes Feld", self.fehler(mit(project__pfad="/tmp")))
        self.assertIn("delivery.owner: unbekanntes Feld", self.fehler(mit(delivery__owner="x")))

    def test_fehlende_felder(self):
        self.assertIn("project.slug: fehlt", self.fehler(mit(project__slug=None)))
        self.assertIn("delivery: fehlt", self.fehler(mit(delivery=None)))

    def test_schema_version(self):
        self.assertIn("schema_version", self.fehler(mit(schema_version=2)))
        self.assertIn("schema_version", self.fehler(mit(schema_version=True)))

    def test_slug(self):
        for slug in ("Beispiel", "-a", "a-", "a--b", "a_b", "../x", "a/b", "", "x" * 41, 7):
            self.assertIn("project.slug", self.fehler(mit(project__slug=slug)), slug)

    def test_package(self):
        for package in ("Beispiel", "1abc", "a-b", "class", "json", "os", "", 5):
            self.assertIn("project.package", self.fehler(mit(project__package=package)), package)

    def test_name(self):
        for name in ("", "   ", "a/b", "a\\b", "..", "{{package}}", "x`id`", "$(id)", "a\nb", "x" * 81, 3):
            self.assertIn("project.name", self.fehler(mit(project__name=name)), repr(name))

    def test_umlaute_im_namen_erlaubt(self):
        a.pruefen(mit(project__name="Stromzähler-Übersicht"), KATALOG)

    def test_template(self):
        self.assertIn("template.id: unbekannt", self.fehler(mit(template__id="ha-integration")))
        self.assertIn("template.version", self.fehler(mit(template__version=2)))

    def test_features(self):
        self.assertIn("features.storage", self.fehler(mit(features__storage="postgresql")))
        self.assertIn("features.storage: fehlt", self.fehler(mit(features={})))
        self.assertIn("features.ui: gibt es", self.fehler(mit(features__ui="web")))

    def test_delivery(self):
        self.assertIn("delivery.github", self.fehler(mit(delivery__github="ja")))

    def test_alle_befunde_auf_einmal(self):
        text = self.fehler(mit(project__slug="X", template__version=9, delivery__github=1))
        for teil in ("project.slug", "template.version", "delivery.github"):
            self.assertIn(teil, text)


class LadenTest(unittest.TestCase):
    def test_kaputtes_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "auftrag.json"
            p.write_text("{kaputt", encoding="utf-8")
            with self.assertRaises(a.AuftragFehler) as ctx:
                a.laden(p, KATALOG)
            self.assertIn("kein gültiges JSON", ctx.exception.fehler[0])

    def test_mit_bom(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "auftrag.json"
            p.write_bytes(b"\xef\xbb\xbf" + json.dumps(GUT).encode("utf-8"))
            self.assertEqual(a.laden(p, KATALOG), GUT)


class ZielTest(unittest.TestCase):
    def test_ziel_in_der_ablage(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(a.zielordner(tmp, "neu"), Path(tmp).resolve() / "neu")

    def test_ziel_existiert(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "neu").mkdir()
            with self.assertRaises(a.AuftragFehler):
                a.zielordner(tmp, "neu")

    def test_ablage_fehlt(self):
        with self.assertRaises(a.AuftragFehler):
            a.zielordner("/gibt/es/nicht", "neu")

    @unittest.skipIf(os.name == "nt", "Symlinks brauchen unter Windows Rechte")
    def test_verknuepfung_als_ziel(self):
        with tempfile.TemporaryDirectory() as tmp, tempfile.TemporaryDirectory() as fremd:
            os.symlink(fremd, Path(tmp) / "neu")
            with self.assertRaises(a.AuftragFehler):
                a.zielordner(tmp, "neu")


if __name__ == "__main__":
    unittest.main()
