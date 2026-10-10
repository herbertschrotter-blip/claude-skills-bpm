"""Tests für checks.py: python3 -m unittest discover -s skills/git-commit-helper/scripts/tests"""

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import checks as c

PY = sys.executable.replace("\\", "/")
PROFIL = f"""# Demo

## Skill-Profil

- Profil-Version: 1

### Checks
- logik: {PY} -c "print('logik')" [src/**; pyproject.toml]
- doku: {PY} -c "print('doku; ok')" [docs/**]
- immer: {PY} -c "print('immer')"
- rot: {PY} -c "import sys; print('kaputt'); sys.exit(3)" [src/**]
- langsam-a: {PY} -c "import time; time.sleep(1)" [src/**]
- langsam-b: {PY} -c "import time; time.sleep(1)" [src/**]
- schwer: {PY} -c "print('allein')" (allein) [src/**]
- kette: cd src && {PY} -c "import os; print(os.path.basename(os.getcwd()))"; {PY} -c "print('zwei')" [src/**]
- fehlt: befehl-den-es-nicht-gibt-xyz [src/**]

### Commit
- Pre-Commit-Checks: logik; doku; immer

## Danach

### Checks
- fremd: nicht aus dem Profil [**]
"""


def git(wurzel, *args):
    subprocess.run(["git", *args], cwd=wurzel, check=True, capture_output=True)


class ProfilTest(unittest.TestCase):
    def test_checks_und_vor_commit(self):
        p = c.profil_lesen(PROFIL)
        self.assertEqual(p["vor_commit"], ["logik", "doku", "immer"])
        self.assertEqual(p["checks"]["logik"]["muster"], ["src/**", "pyproject.toml"])
        self.assertEqual(p["checks"]["immer"]["muster"], [])
        self.assertTrue(p["checks"]["schwer"]["allein"])
        self.assertNotIn("fremd", p["checks"])
        self.assertEqual(len(p["checks"]["kette"]["befehle"]), 2)
        self.assertEqual(len(p["checks"]["doku"]["befehle"]), 1)  # Semikolon in Anführungszeichen

    def test_ohne_profil(self):
        with self.assertRaises(c.ProfilFehler):
            c.profil_lesen("# nur Text\n")

    def test_muster(self):
        dateien = {"src/a.py", "src/x/b.py", "README.md", "a.py", "docs/n.md"}
        self.assertEqual(c.passende(dateien, ["src/**"]), ["src/a.py", "src/x/b.py"])
        self.assertEqual(c.passende(dateien, ["**/*.py"]), ["a.py", "src/a.py", "src/x/b.py"])
        self.assertEqual(c.passende(dateien, ["*.md"]), ["README.md"])
        self.assertEqual(c.passende(dateien, []), sorted(dateien))


class LaufTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.wurzel = self.tmp.name
        git(self.wurzel, "init", "-q")
        (Path(self.wurzel) / "src").mkdir()
        (Path(self.wurzel) / "src" / "a.py").write_text("x = 1\n", encoding="utf-8")
        self.profil = c.profil_lesen(PROFIL)

    def lauf(self, namen, **kw):
        return {e["name"]: e for e in c.laufen(self.wurzel, self.profil, namen, c.geaendert(self.wurzel), **kw)}

    def test_nur_passende_und_ohne_muster_immer(self):
        r = self.lauf(["logik", "doku", "immer"])
        self.assertEqual(r["logik"]["ergebnis"], "grün")
        self.assertEqual(r["doku"]["ergebnis"], "übersprungen")
        self.assertEqual(r["immer"]["ergebnis"], "grün")

    def test_schon_gruen_bis_zur_aenderung(self):
        self.lauf(["logik"])
        self.assertEqual(self.lauf(["logik"])["logik"]["ergebnis"], "schon grün")
        self.assertEqual(self.lauf(["logik"], immer=True)["logik"]["ergebnis"], "grün")
        (Path(self.wurzel) / "src" / "a.py").write_text("x = 2\n", encoding="utf-8")
        self.assertEqual(self.lauf(["logik"])["logik"]["ergebnis"], "grün")

    def test_rot_mit_ausgabe_und_ohne_merker(self):
        r = self.lauf(["rot"])["rot"]
        self.assertEqual((r["ergebnis"], r["exit"]), ("rot", 3))
        self.assertIn("kaputt", r["ausgabe"])
        self.assertEqual(self.lauf(["rot"])["rot"]["ergebnis"], "rot")  # rot wird nie gemerkt

    def test_parallel(self):
        start = time.monotonic()
        r = self.lauf(["langsam-a", "langsam-b"])
        self.assertLess(time.monotonic() - start, 1.9)
        self.assertEqual({e["ergebnis"] for e in r.values()}, {"grün"})

    def test_allein_und_kette(self):
        r = self.lauf(["schwer", "kette"])
        self.assertEqual(r["schwer"]["ergebnis"], "grün")
        log = Path(r["kette"]["log"]).read_text(encoding="utf-8")
        self.assertEqual(log.split(), ["src", "zwei"])

    @unittest.skipIf(os.name == "nt", "Exit 127 der POSIX-Shell")
    def test_befehl_fehlt(self):
        r = self.lauf(["fehlt", "logik"])
        self.assertEqual(r["fehlt"]["ergebnis"], "fehlt")
        self.assertEqual(c.exit_code(list(r.values())), 2)

    def test_fehlertext_allein_ist_kein_fehlender_befehl(self):
        check = {"befehle": [f"{PY} -c \"print('x is not recognized as y'); raise SystemExit(1)\""], "muster": [],
                 "allein": False}
        r = c.ausfuehren("t", check, self.wurzel, self.wurzel)
        self.assertEqual(r["ergebnis"], "rot")

    def test_zeitlimit_wird_genannt(self):
        check = {"befehle": [f"{PY} -c \"print('vorher', flush=True); import time; time.sleep(5)\""], "muster": [],
                 "allein": False}
        alt, c.TIMEOUT = c.TIMEOUT, 1
        try:
            r = c.ausfuehren("t", check, self.wurzel, self.wurzel)
        finally:
            c.TIMEOUT = alt
        self.assertEqual(r["ergebnis"], "rot")
        self.assertTrue(r["ausgabe"].startswith("Zeitlimit 1 s überschritten"), r["ausgabe"])

    def test_unbekannter_check_ist_fehler(self):
        r = c.laufen(self.wurzel, self.profil, ["gibtsnicht"], set())
        self.assertEqual(r[0]["ergebnis"], "unbekannt")
        self.assertEqual(c.exit_code(r), 1)

    def test_merker_liegt_in_git(self):
        self.lauf(["logik"])
        merker = Path(self.wurzel) / ".git" / c.MERKER
        self.assertIn("logik", json.loads(merker.read_text(encoding="utf-8")))
        self.assertNotIn(c.MERKER, " ".join(c.geaendert(self.wurzel)))

    def test_tabelle(self):
        r = c.laufen(self.wurzel, self.profil, ["logik", "doku"], c.geaendert(self.wurzel))
        text = c.tabelle(r)
        self.assertIn("| logik | 0:00 | grün |", text)
        self.assertIn("| doku | – | übersprungen – keine passende Datei |", text)


if __name__ == "__main__":
    unittest.main()
