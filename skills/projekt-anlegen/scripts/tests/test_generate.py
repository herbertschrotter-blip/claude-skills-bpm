"""Tests für generate.py mit dem mitgelieferten Katalog: python3 -m unittest discover -s skills/projekt-anlegen/scripts/tests

Hier nur, was ohne Netz und ohne Zusatzpakete geht (Dateien, Herkunft, Syntax, Start). Format, Lint und die Tests
der erzeugten Projekte prüft die Verifikation (Schritt Verify) bzw. die CI des Generators."""

import json
import os
import subprocess
import sys
import tempfile
import tomllib
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import generate as g  # noqa: E402
from auftrag import AuftragFehler  # noqa: E402


def auftrag(storage="sqlite", github=True, name="Stromzähler Übersicht"):
    return {
        "schema_version": 1,
        "project": {"name": name, "slug": "stromzaehler", "package": "stromzaehler"},
        "template": {"id": "python-tool", "version": 1},
        "features": {"storage": storage},
        "delivery": {"github": github},
    }


class ErzeugenTest(unittest.TestCase):
    def erzeugen(self, **kw):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        dateien = g.erzeugen(auftrag(**kw), tmp.name)
        return Path(tmp.name), dateien

    def test_dateien_mit_sqlite_und_github(self):
        root, dateien = self.erzeugen()
        for datei in ("CLAUDE.md", "pyproject.toml", "stromzaehler/speicher.py", "tests/test_speicher.py",
                      ".github/workflows/ci.yml", "docs/entscheidungen.md", ".projekt-anlegen.json"):
            self.assertIn(datei, dateien)
            self.assertTrue((root / datei).is_file(), datei)
        self.assertIn("SCHEMA_VERSION", (root / "stromzaehler/speicher.py").read_text(encoding="utf-8"))

    def test_ohne_speicher_ohne_github(self):
        root, dateien = self.erzeugen(storage="none", github=False)
        self.assertNotIn(".github/workflows/ci.yml", dateien)
        self.assertNotIn("sqlite", (root / "stromzaehler/speicher.py").read_text(encoding="utf-8").lower())

    def test_keine_platzhalter_uebrig_und_lf(self):
        root, dateien = self.erzeugen()
        for datei in dateien:
            roh = (root / datei).read_bytes()
            self.assertNotIn(b"{{", roh, datei)
            self.assertNotIn(b"\r\n", roh, datei)

    def test_pyproject_gueltig_mit_versionen(self):
        root, _ = self.erzeugen()
        data = tomllib.loads((root / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertEqual(data["project"]["name"], "stromzaehler")
        self.assertEqual(data["project"]["description"], "Stromzähler Übersicht")
        self.assertTrue(all("==" in d for d in data["project"]["optional-dependencies"]["dev"]))

    def test_herkunft_ohne_datum_und_gleich(self):
        root1, _ = self.erzeugen()
        root2, _ = self.erzeugen()
        a, b = ((r / g.HERKUNFT).read_text(encoding="utf-8") for r in (root1, root2))
        self.assertEqual(a, b)
        self.assertEqual(json.loads(a)["components"], ["common", "python-tool", "storage-sqlite", "ci-github-python"])

    def test_gleicher_auftrag_gleiche_dateien(self):
        root1, dateien = self.erzeugen()
        root2, _ = self.erzeugen()
        for datei in dateien:
            self.assertEqual((root1 / datei).read_bytes(), (root2 / datei).read_bytes(), datei)

    def test_start_beider_varianten(self):
        for storage in ("none", "sqlite"):
            root, _ = self.erzeugen(storage=storage)
            with tempfile.TemporaryDirectory() as daten:
                env = dict(os.environ, STROMZAEHLER_DATEN=daten)
                r = subprocess.run([sys.executable, "-m", "stromzaehler", "status"], cwd=root, env=env,
                                   capture_output=True, text=True, timeout=60, check=False)
            self.assertEqual(r.returncode, 0, r.stderr)
            self.assertEqual(json.loads(r.stdout), {"status": "ready"})

    def test_ordner_nicht_leer(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "da.txt").write_text("x", encoding="utf-8")
            with self.assertRaises(AuftragFehler):
                g.erzeugen(auftrag(), tmp)
            self.assertEqual(os.listdir(tmp), ["da.txt"])

    def test_ungueltiger_auftrag_schreibt_nichts(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(AuftragFehler):
                g.erzeugen(auftrag(storage="postgresql"), tmp)
            self.assertEqual(os.listdir(tmp), [])



class HaIntegrationTest(unittest.TestCase):
    """Projektart ha-integration: Dateien beider Quellen; die HA-Tests selbst laufen in der Verifikation."""

    def erzeugen(self, quelle):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        daten = {
            "schema_version": 1,
            "project": {"name": "Rasen Planer", "slug": "ha-rasen", "package": "rasen"},
            "template": {"id": "ha-integration", "version": 1},
            "features": {"quelle": quelle},
            "delivery": {"github": True},
        }
        return Path(tmp.name), g.erzeugen(daten, tmp.name)

    def test_aufsatz(self):
        root, dateien = self.erzeugen("aufsatz")
        manifest = json.loads((root / "custom_components/rasen/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual((manifest["domain"], manifest["iot_class"]), ("rasen", "calculated"))
        self.assertNotIn("custom_components/rasen/coordinator.py", dateien)
        self.assertIn("aufsatz", (root / "docs/entscheidungen.md").read_text(encoding="utf-8"))

    def test_abruf(self):
        root, dateien = self.erzeugen("abruf")
        manifest = json.loads((root / "custom_components/rasen/manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["iot_class"], "local_polling")
        for datei in ("custom_components/rasen/coordinator.py", "custom_components/rasen/api.py",
                      "tests/logik/test_api.py", ".github/workflows/ci.yml", "hacs.json"):
            self.assertIn(datei, dateien)

    def test_python_dateien_sind_gueltig(self):
        for quelle in ("aufsatz", "abruf"):
            root, dateien = self.erzeugen(quelle)
            for datei in (d for d in dateien if d.endswith(".py")):
                compile((root / datei).read_text(encoding="utf-8"), datei, "exec")


if __name__ == "__main__":
    unittest.main()
