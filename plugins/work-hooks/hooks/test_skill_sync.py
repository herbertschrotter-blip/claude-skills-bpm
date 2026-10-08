#!/usr/bin/env python3
"""Tests für skill_sync.py (nur Standardbibliothek): python3 -m unittest plugins/work-hooks/hooks/test_skill_sync.py"""

import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import skill_sync as s  # noqa: E402


class SyncTest(unittest.TestCase):
    def test_kopiert_nur_monatsdateien_und_nur_geaenderte(self):
        with tempfile.TemporaryDirectory() as src, tempfile.TemporaryDirectory() as dst:
            for name in ("2026-10.jsonl", "raw-2026-10.jsonl", "statistik.html"):
                with open(os.path.join(src, name), "w") as fh:
                    fh.write("x\n")
            self.assertEqual(s.copy_own(src, dst), 1)
            self.assertEqual(sorted(os.listdir(dst)), ["2026-10.jsonl"])
            self.assertEqual(s.copy_own(src, dst), 0)
            with open(os.path.join(src, "2026-10.jsonl"), "a") as fh:
                fh.write("y\n")
            self.assertEqual(s.copy_own(src, dst), 1)

    def test_ohne_repo_passiert_nichts(self):
        env = {k: v for k, v in os.environ.items() if k not in ("SKILL_LOG_REPO", "CLAUDE_PLUGIN_OPTION_LOG_REPO")}
        result = subprocess.run([sys.executable, os.path.join(HERE, "skill_sync.py")], input="{}", text=True,
                                capture_output=True, env=env, timeout=10)
        self.assertEqual((result.returncode, result.stdout), (0, ""))

    def test_ungueltiger_repo_name_wird_ignoriert(self):
        env = dict(os.environ, SKILL_LOG_REPO="kein repo; rm -rf /")
        result = subprocess.run([sys.executable, os.path.join(HERE, "skill_sync.py")], input="{}", text=True,
                                capture_output=True, env=env, timeout=10)
        self.assertEqual(result.returncode, 0)

    def test_rechnername_ohne_sonderzeichen(self):
        old = os.environ.get("SKILL_LOG_HOST")
        os.environ["SKILL_LOG_HOST"] = "firmen laptop/1"
        try:
            self.assertEqual(s.host_name(), "firmen_laptop_1")
        finally:
            if old is None:
                os.environ.pop("SKILL_LOG_HOST")
            else:
                os.environ["SKILL_LOG_HOST"] = old


if __name__ == "__main__":
    unittest.main()
