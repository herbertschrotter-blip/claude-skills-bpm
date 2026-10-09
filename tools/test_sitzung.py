#!/usr/bin/env python3
"""Tests für skills/sitzung/scripts/sitzung.py (nur Standardbibliothek): python3 -m unittest tools/test_sitzung.py"""

import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "skills", "sitzung", "scripts"))
import sitzung as z  # noqa: E402


class EigenesFensterTest(unittest.TestCase):
    def setUp(self):
        self.calls, self._sh, self._env = [], z.sh, dict(os.environ)
        z.sh = lambda *args, **kw: self.calls.append(args) or "@5\n"

    def tearDown(self):
        z.sh = self._sh
        os.environ.clear()
        os.environ.update(self._env)

    def test_fragt_den_eigenen_bereich(self):
        os.environ.update(TMUX="/tmp/tmux-0/default,1,0", TMUX_PANE="%2")
        self.assertEqual(z.tmux_eigen("#{window_id}"), "@5")
        self.assertEqual(self.calls[-1], ("tmux", "display-message", "-p", "-t", "%2", "#{window_id}"))

    def test_ohne_tmux_leer(self):
        os.environ.pop("TMUX", None)
        self.assertEqual(z.tmux_eigen("#S"), "")
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
