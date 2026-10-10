"""Tests für pruefung.py: python3 -m unittest discover -s skills/projekt-anlegen/scripts/tests"""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import pruefung as p  # noqa: E402

PY = "{python}"
PRUEFUNG = {
    "einrichten": [],
    "checks": [
        {"name": "ueberall", "befehl": [PY, "-c", "print('ok')"]},
        {"name": "nur-linux", "plattform": ["linux"], "befehl": [PY, "-c", "raise SystemExit(1)"]},
    ],
}


class PlattformTest(unittest.TestCase):
    def lauf(self, name):
        with tempfile.TemporaryDirectory() as tmp, mock.patch.object(p, "plattform", return_value=name):
            return p.ausfuehren(PRUEFUNG, tmp, "demo")

    def test_check_anderer_plattform_wird_uebersprungen(self):
        ok, ergebnisse = self.lauf("windows")
        self.assertTrue(ok)
        self.assertEqual(ergebnisse[-1], {"name": "nur-linux", "dauer": 0.0, "ok": True, "uebersprungen": "nur linux"})

    def test_check_eigener_plattform_laeuft(self):
        ok, ergebnisse = self.lauf("linux")
        self.assertFalse(ok)
        self.assertEqual(ergebnisse[-1]["name"], "nur-linux")

    def test_unbekannte_plattform_ist_befund(self):
        befunde = p.tokens_pruefen({"checks": [{"name": "x", "plattform": ["amiga"], "befehl": []}]})
        self.assertIn("Prüfschritt x: plattform nur aus linux, macos, windows", befunde)


if __name__ == "__main__":
    unittest.main()
