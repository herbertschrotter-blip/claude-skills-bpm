"""Tests für bausteine.py und validate.py: python3 -m unittest discover -s skills/projekt-anlegen/scripts/tests"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import auftrag as a  # noqa: E402
import bausteine as b  # noqa: E402
import validate as v  # noqa: E402

ART = {
    "id": "werkzeug", "version": 1, "components": ["basis", "kern"],
    "features": {"storage": {"none": [], "sqlite": ["db"]}},
    "delivery": {"github": ["ci"]},
    "kombinationen": [{"storage": "none"}, {"storage": "sqlite"}],
}
KATALOG = {
    "basis": {"id": "basis", "requires": [], "files": [{"source": "basis/README.md.tpl", "target": "README.md"}]},
    "kern": {"id": "kern", "requires": ["basis"],
             "files": [{"source": "kern/main.py.tpl", "target": "src/{{package}}/__main__.py"}]},
    "db": {"id": "db", "requires": ["kern"], "files": [{"source": "db/store.py.tpl", "target": "src/{{package}}/store.py"}]},
    "ci": {"id": "ci", "requires": ["basis"], "files": [{"source": "ci/ci.yml.tpl", "target": ".github/workflows/ci.yml"}]},
}
AUFTRAG = {
    "schema_version": 1,
    "project": {"name": "Stromzähler", "slug": "stromzaehler", "package": "stromzaehler"},
    "template": {"id": "werkzeug", "version": 1},
    "features": {"storage": "sqlite"},
    "delivery": {"github": True},
}


def katalog_ordner(tmp, katalog=KATALOG, art=ART, inhalte=None):
    """Legt einen Katalog mit Manifesten und Vorlagen in tmp an."""
    root = Path(tmp)
    (root / "manifests" / "components").mkdir(parents=True)
    (root / "manifests" / f"{art['id']}.json").write_text(json.dumps(art), encoding="utf-8", newline="\n")
    for cid, data in katalog.items():
        (root / "manifests" / "components" / f"{cid}.json").write_text(json.dumps(data), encoding="utf-8",
                                                                       newline="\n")
        for f in data.get("files", []):
            datei = root / f["source"]
            datei.parent.mkdir(parents=True, exist_ok=True)
            datei.write_text((inhalte or {}).get(f["source"], "# {{name}}\n"), encoding="utf-8", newline="\n")
    return root


class AuswahlTest(unittest.TestCase):
    def test_grund_feature_und_github(self):
        self.assertEqual(b.auswahl(AUFTRAG, ART), ["basis", "kern", "db", "ci"])

    def test_ohne_speicher_ohne_github(self):
        auftrag = dict(AUFTRAG, features={"storage": "none"}, delivery={"github": False})
        self.assertEqual(b.auswahl(auftrag, ART), ["basis", "kern"])

    def test_kombination_nicht_freigegeben(self):
        art = dict(ART, kombinationen=[{"storage": "none"}])
        with self.assertRaises(a.AuftragFehler) as ctx:
            a.pruefen(AUFTRAG, {"werkzeug": art})
        self.assertIn("nicht freigegeben", ctx.exception.fehler[0])


class AufloesenTest(unittest.TestCase):
    def test_voraussetzungen_zuerst(self):
        self.assertEqual(b.aufloesen(["db"], KATALOG), ["basis", "kern", "db"])

    def test_unbekannt(self):
        katalog = dict(KATALOG, kern=dict(KATALOG["kern"], requires=["fehlt"]))
        with self.assertRaises(a.AuftragFehler) as ctx:
            b.aufloesen(["kern"], katalog)
        self.assertIn("Baustein fehlt: unbekannt (verlangt von kern)", ctx.exception.fehler)

    def test_zyklus(self):
        katalog = dict(KATALOG, basis=dict(KATALOG["basis"], requires=["db"]))
        with self.assertRaises(a.AuftragFehler) as ctx:
            b.aufloesen(["db"], katalog)
        self.assertTrue(any(f.startswith("Zyklus:") for f in ctx.exception.fehler))

    def test_konflikt(self):
        katalog = dict(KATALOG, ci=dict(KATALOG["ci"], conflicts=["db"]))
        with self.assertRaises(a.AuftragFehler) as ctx:
            b.aufloesen(["db", "ci"], katalog)
        self.assertIn("Konflikt: ci verträgt sich nicht mit db", ctx.exception.fehler)


class PlatzhalterTest(unittest.TestCase):
    def test_ersetzen(self):
        self.assertEqual(b.ersetzen("# {{ name }} ({{package}})", b.werte(AUFTRAG)), "# Stromzähler (stromzaehler)")

    def test_unbekannt(self):
        with self.assertRaises(a.AuftragFehler):
            b.ersetzen("{{owner}}", b.werte(AUFTRAG))

    def test_feature_als_platzhalter(self):
        werte = b.werte(dict(AUFTRAG, features={"storage": "sqlite", "quelle": "abruf"}))
        self.assertEqual(b.ersetzen("{{storage}}/{{quelle}}", werte), "sqlite/abruf")
        self.assertEqual(b.feature_namen({"x": ART}), {"storage"})

    def test_wert_wird_nicht_erneut_ersetzt(self):
        werte = dict(b.werte(AUFTRAG), name="{{slug}}")
        self.assertEqual(b.ersetzen("{{name}}", werte), "{{slug}}")


class DateiplanTest(unittest.TestCase):
    def test_plan(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = katalog_ordner(tmp)
            plan = b.dateiplan(["basis", "kern", "db"], KATALOG, b.werte(AUFTRAG), root)
        self.assertEqual([z for _, z in plan], ["README.md", "src/stromzaehler/__main__.py", "src/stromzaehler/store.py"])

    def test_doppelte_zieldatei(self):
        katalog = dict(KATALOG, db=dict(KATALOG["db"], files=[{"source": "db/store.py.tpl", "target": "readme.md"}]))
        with tempfile.TemporaryDirectory() as tmp:
            root = katalog_ordner(tmp, katalog)
            with self.assertRaises(a.AuftragFehler) as ctx:
                b.dateiplan(["basis", "kern", "db"], katalog, b.werte(AUFTRAG), root)
        self.assertIn("schreiben basis und db", ctx.exception.fehler[0])

    def test_ziel_ausserhalb(self):
        for ziel in ("../aussen.py", "/etc/x", "C:/x", "a\\b", ""):
            katalog = dict(KATALOG, basis=dict(KATALOG["basis"], files=[{"source": "basis/README.md.tpl", "target": ziel}]))
            with tempfile.TemporaryDirectory() as tmp:
                root = katalog_ordner(tmp, katalog)
                with self.assertRaises(a.AuftragFehler, msg=ziel):
                    b.dateiplan(["basis"], katalog, b.werte(AUFTRAG), root)

    def test_vorlage_fehlt(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = katalog_ordner(tmp)
            (root / "kern" / "main.py.tpl").unlink()
            with self.assertRaises(a.AuftragFehler) as ctx:
                b.dateiplan(["basis", "kern"], KATALOG, b.werte(AUFTRAG), root)
        self.assertIn("Vorlage kern/main.py.tpl fehlt", ctx.exception.fehler[0])


class KatalogTest(unittest.TestCase):
    def test_mitgelieferter_katalog(self):
        self.assertEqual(v.pruefen(), [])

    def test_guter_katalog(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(v.pruefen(katalog_ordner(tmp)), [])

    def test_befunde(self):
        inhalte = {
            "basis/README.md.tpl": "Pfad /config/projekte/x und {{owner}}\r\n",
            "kern/main.py.tpl": 'token = "abcdef123"\n',
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = katalog_ordner(tmp, inhalte=inhalte)
            (root / "db" / "store.py.tpl").write_bytes(b"\xef\xbb\xbfx\n")
            text = " | ".join(v.pruefen(root))
        for teil in ("absoluter Pfad", "{{owner}}", "CRLF", "Zugangsdaten", "BOM"):
            self.assertIn(teil, text)

    def test_kaputte_kombination(self):
        art = dict(ART, features={"storage": {"none": [], "sqlite": ["gibtsnicht"]}})
        with tempfile.TemporaryDirectory() as tmp:
            befunde = v.pruefen(katalog_ordner(tmp, art=art))
        self.assertTrue(any("gibtsnicht: unbekannt" in x for x in befunde))


if __name__ == "__main__":
    unittest.main()
