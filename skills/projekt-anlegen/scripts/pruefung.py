"""Prüfschritte eines erzeugten Projekts ausführen (nur Standardbibliothek).

Die Befehle stehen deklarativ im Manifest der Projektart (`pruefung`: `einrichten` und `checks`), nie im Auftrag.
Als Platzhalter gibt es nur {python} (dieser Interpreter), {venv_python} (Interpreter der .venv im Projekt),
{package}, {package_upper} und {tmp} (eigener leerer Ordner je Check). Ausgeführt wird ohne Shell.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

TOKEN = re.compile(r"\{([a-z_]+)\}")
TOKENS = {"python", "venv_python", "package", "package_upper", "tmp"}
TIMEOUT = 900  # Sekunden je Befehl; die Installation der Werkzeuge braucht auf dem Pi am längsten


def venv_python(projekt):
    if os.name == "nt":
        return Path(projekt) / ".venv" / "Scripts" / "python.exe"
    return Path(projekt) / ".venv" / "bin" / "python"


def _einsetzen(text, werte):
    def eins(match):
        key = match.group(1)
        if key not in TOKENS or key not in werte:
            raise ValueError(f"unbekannter Platzhalter {{{key}}} in einem Prüfbefehl")
        return str(werte[key])

    return TOKEN.sub(eins, text)


def tokens_pruefen(pruefung):
    """Befunde zu unbekannten Platzhaltern in einem `pruefung`-Abschnitt (für validate.py)."""
    befunde = []
    texte = [t for befehl in pruefung.get("einrichten", []) for t in befehl]
    for check in pruefung.get("checks", []):
        texte += list(check.get("befehl", [])) + list(check.get("umgebung", {})) + list(check.get("umgebung", {}).values())
    for text in texte:
        for key in TOKEN.findall(text):
            if key not in TOKENS:
                befunde.append(f"Prüfbefehl: unbekannter Platzhalter {{{key}}}")
    return befunde


def _lauf(befehl, cwd, env):
    start = time.monotonic()
    try:
        r = subprocess.run(befehl, cwd=cwd, env=env, capture_output=True, text=True, timeout=TIMEOUT,
                           check=False, shell=False)
        code, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        code, out, err = -1, "", f"Zeitlimit {TIMEOUT} s überschritten"
    except OSError as exc:
        code, out, err = -1, "", str(exc)
    return code, out, err, time.monotonic() - start


def ausfuehren(pruefung, projekt, package):
    """Richtet die Umgebung ein und führt alle Checks aus. Gibt (ok, Ergebnisse) zurück; Ergebnisse je Schritt mit
    name, dauer (s), ok und bei Fehler den letzten Zeilen der Ausgabe. Bricht beim ersten Fehler ab."""
    projekt = Path(projekt)
    werte = {"python": sys.executable, "venv_python": venv_python(projekt), "package": package,
             "package_upper": package.upper()}
    basis_env = {k: v for k, v in os.environ.items() if not k.startswith("PYTHON")}
    ergebnisse = []
    schritte = [{"name": "einrichten", "befehle": pruefung.get("einrichten", [])}]
    schritte += [dict(c, befehle=[c["befehl"]]) for c in pruefung.get("checks", [])]
    for schritt in schritte:
        with tempfile.TemporaryDirectory() as tmp:
            werte["tmp"] = tmp
            env = dict(basis_env)
            for key, value in schritt.get("umgebung", {}).items():
                env[_einsetzen(key, werte)] = _einsetzen(value, werte)
            dauer, ok, rest = 0.0, True, ""
            for befehl in schritt["befehle"]:
                code, out, err, sek = _lauf([_einsetzen(t, werte) for t in befehl], projekt, env)
                dauer += sek
                if code != 0:
                    ok, rest = False, "\n".join((out + err).strip().splitlines()[-15:])
                    break
                if "ausgabe_json" in schritt:
                    try:
                        gleich = json.loads(out) == schritt["ausgabe_json"]
                    except json.JSONDecodeError:
                        gleich = False
                    if not gleich:
                        ok, rest = False, f"erwartet {json.dumps(schritt['ausgabe_json'])}, erhalten: {out.strip()[:300]}"
                        break
        ergebnisse.append({"name": schritt["name"], "dauer": round(dauer, 1), "ok": ok, **({"ausgabe": rest} if rest else {})})
        if not ok:
            return False, ergebnisse
    return True, ergebnisse
