import json
import os
import subprocess
import sys
from pathlib import Path

from {{package}}.cli import main

PROJEKT = Path(__file__).resolve().parent.parent


def test_status(daten, capsys):
    assert main(["status"]) == 0
    assert json.loads(capsys.readouterr().out) == {"status": "ready"}


def test_leere_einstellung(monkeypatch, capsys):
    monkeypatch.setenv("{{package_upper}}_DATEN", "  ")
    assert main(["status"]) == 2
    assert "Einstellungen" in capsys.readouterr().err


def test_start_als_programm(daten):
    """Starttest: das Programm läuft als eigener Prozess, wie beim Nutzer."""
    umgebung = dict(os.environ, {{package_upper}}_DATEN=str(daten))
    ergebnis = subprocess.run(
        [sys.executable, "-m", "{{package}}", "status"],
        cwd=PROJEKT,
        env=umgebung,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert ergebnis.returncode == 0, ergebnis.stderr
    assert json.loads(ergebnis.stdout) == {"status": "ready"}
