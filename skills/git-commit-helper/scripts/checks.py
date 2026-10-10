#!/usr/bin/env python3
"""Prüfläufe vor dem Commit nach dem Skill-Profil (nur Standardbibliothek).

Liest `### Checks` und `Pre-Commit-Checks` aus dem Skill-Profil der `CLAUDE.md` (docs/skill-profile-v1.md), nimmt die
geänderten Dateien aus git, lässt nur passende Checks laufen und meldet eine Tabelle Check / Dauer / Ergebnis.
Regeln: skills/git-commit-helper/SKILL.md, Abschnitt „Prüfläufe vor dem Commit“.

    python3 checks.py --vor-commit            # Pre-Commit-Checks, die für die Änderung gelten
    python3 checks.py --checks logik,lint     # bestimmte Checks (auch nur, wenn sie gelten)
    python3 checks.py --vor-commit --json     # Ergebnis als JSON

- Befehle eines Checks laufen nacheinander in einer Shell (`cd` gilt für die folgenden), Abbruch beim ersten Fehler.
- Checks laufen gleichzeitig; ein Check mit `(allein)` im Profil läuft danach für sich (z. B. Tests auf allen Kernen).
- Ein Check, der mit demselben Stand der passenden Dateien schon grün war, läuft nicht noch einmal (`--immer` erzwingt
  es). Der Merker liegt in `.git/`, nie im Repo.
- Ausgabe je Check in eine Datei; bei Rot stehen die letzten Zeilen im Ergebnis.

Exit 0: nichts rot und kein Befehl fehlt. 1: mindestens ein Check rot. 2: nichts rot, aber ein Befehl fehlt auf diesem
Rechner (z. B. pwsh); der Check muss dann woanders laufen. 3: Profil oder git nicht lesbar.
"""

import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

TIMEOUT = 1800  # Sekunden je Check
MERKER = "skill-checks.json"
_CHECK = re.compile(r"^-\s+([\w.-]+):\s*(.*?)\s*$")
_MUSTER = re.compile(r"\s*\[([^\[\]]*)\]\s*$")
_ALLEIN = re.compile(r"\s*\(allein\)\s*$")


class ProfilFehler(Exception):
    pass


def abschnitt(text, ueberschrift, ebene):
    """Zeilen unter einer Überschrift bis zur nächsten gleicher oder höherer Ebene."""
    zeilen, drin = [], False
    for zeile in text.splitlines():
        if re.match(rf"^#{{1,{ebene}}}\s", zeile):
            if drin:
                break
            drin = zeile.strip() == ueberschrift
            continue
        if drin:
            zeilen.append(zeile)
    return zeilen if drin or zeilen else None


def befehle_teilen(text):
    """`a; b` → [a, b]; Semikolons in Anführungszeichen bleiben stehen."""
    teile, aktuell, quote = [], "", None
    for zeichen in text:
        if quote:
            quote = None if zeichen == quote else quote
        elif zeichen in "'\"":
            quote = zeichen
        elif zeichen == ";":
            teile.append(aktuell.strip())
            aktuell = ""
            continue
        aktuell += zeichen
    teile.append(aktuell.strip())
    return [t for t in teile if t]


def profil_lesen(text):
    """{'checks': {name: {befehle, muster, allein}}, 'vor_commit': [namen]} aus einer CLAUDE.md."""
    profil = abschnitt(text, "## Skill-Profil", 2)
    if profil is None:
        raise ProfilFehler("kein Abschnitt „## Skill-Profil“ in der CLAUDE.md")
    profil_text = "\n".join(profil)
    checks = {}
    for zeile in abschnitt(profil_text, "### Checks", 3) or []:
        m = _CHECK.match(zeile)
        if not m or m.group(2) in ("", "none"):
            continue
        rest, muster = m.group(2), []
        mm = _MUSTER.search(rest)
        if mm:
            muster = [p.strip() for p in mm.group(1).split(";") if p.strip()]
            rest = rest[: mm.start()]
        allein = bool(_ALLEIN.search(rest))
        rest = _ALLEIN.sub("", rest)
        checks[m.group(1)] = {"befehle": befehle_teilen(rest), "muster": muster, "allein": allein}
    vor_commit = []
    for zeile in abschnitt(profil_text, "### Commit", 3) or []:
        m = re.match(r"^-\s+Pre-Commit-Checks:\s*(.*?)\s*$", zeile)
        if m and m.group(1) != "none":
            vor_commit = [n.strip() for n in m.group(1).split(";") if n.strip()]
    return {"checks": checks, "vor_commit": vor_commit}


def muster_regex(muster):
    """Pfad-Glob → Regex: `**` beliebig tief (auch null Ordner), `*` und `?` innerhalb eines Ordners."""
    teile, i = [], 0
    while i < len(muster):
        if muster.startswith("**/", i):
            teile.append("(?:.*/)?")
            i += 3
        elif muster.startswith("**", i):
            teile.append(".*")
            i += 2
        elif muster[i] == "*":
            teile.append("[^/]*")
            i += 1
        elif muster[i] == "?":
            teile.append("[^/]")
            i += 1
        else:
            teile.append(re.escape(muster[i]))
            i += 1
    return re.compile("^" + "".join(teile) + "$")


def passende(dateien, muster):
    """Geänderte Dateien, die zu einem der Muster passen; ohne Muster gilt der Check immer (alle Dateien)."""
    if not muster:
        return sorted(dateien)
    regexe = [muster_regex(m) for m in muster]
    return sorted(d for d in dateien if any(r.match(d) for r in regexe))


def geaendert(wurzel):
    """Geänderte Dateien relativ zur Wurzel: gestaged, ungestaged und neu (bei Umbenennung alter und neuer Name)."""
    r = subprocess.run(["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"], cwd=wurzel,
                       capture_output=True, check=False)
    if r.returncode:
        raise ProfilFehler("git status gescheitert: " + r.stderr.decode(errors="replace").strip())
    teile, dateien, i = r.stdout.decode("utf-8", errors="replace").split("\0"), set(), 0
    while i < len(teile):
        eintrag = teile[i]
        if len(eintrag) > 3:
            dateien.add(eintrag[3:])
            if eintrag[0] in "RC":  # Umbenennung: der alte Name folgt als eigener Eintrag
                i += 1
                if i < len(teile) and teile[i]:
                    dateien.add(teile[i])
        i += 1
    return dateien


def fingerabdruck(wurzel, check, dateien):
    """Stand des Checks: Befehle und Inhalt der passenden Dateien (gelöschte als solche)."""
    h = hashlib.sha256(json.dumps(check["befehle"]).encode())
    for datei in dateien:
        pfad = Path(wurzel) / datei
        h.update(datei.encode() + b"\0")
        if pfad.is_file():
            h.update(hashlib.sha256(pfad.read_bytes()).digest())
        else:
            h.update(b"<weg>")
    return h.hexdigest()


def merker_pfad(wurzel):
    r = subprocess.run(["git", "rev-parse", "--git-path", MERKER], cwd=wurzel, capture_output=True, text=True,
                       check=False)
    return Path(wurzel) / r.stdout.strip() if r.returncode == 0 else None


def shell(befehle):
    """Aufruf für die Befehle eines Checks: nacheinander, Abbruch beim ersten Fehler."""
    if os.name != "nt":
        return ["sh", "-c", " && ".join(befehle)]
    if shutil.which("pwsh"):
        return ["pwsh", "-NoProfile", "-Command", " && ".join(befehle)]
    return ["powershell", "-NoProfile", "-Command", "; if (-not $?) { exit 1 }; ".join(befehle)]


def ausfuehren(name, check, wurzel, ordner):
    """Führt einen Check aus; Ausgabe nach <ordner>/<name>.log."""
    log = Path(ordner) / f"{name}.log"
    start = time.monotonic()
    try:
        with open(log, "w", encoding="utf-8", errors="replace") as fh:
            r = subprocess.run(shell(check["befehle"]), cwd=wurzel, stdout=fh, stderr=subprocess.STDOUT,
                               timeout=TIMEOUT, check=False)
        code = r.returncode
    except subprocess.TimeoutExpired:
        code = -1
    except OSError as exc:
        log.write_text(str(exc), encoding="utf-8")
        code = 127
    dauer = round(time.monotonic() - start, 1)
    text = log.read_text(encoding="utf-8", errors="replace")
    if code == 0:
        return {"name": name, "ergebnis": "grün", "dauer": dauer, "log": str(log)}
    # Befehl nicht vorhanden: Exit 127 der POSIX-Shell bzw. die Ausnahme von PowerShell – nicht jeder Text, der so klingt
    fehlt = code == 127 or (os.name == "nt" and "CommandNotFoundException" in text)
    letzte = "\n".join(text.strip().splitlines()[-20:])
    if code == -1:
        letzte = f"Zeitlimit {TIMEOUT} s überschritten" + (f"\n{letzte}" if letzte else "")
    return {"name": name, "ergebnis": "fehlt" if fehlt else "rot", "dauer": dauer, "exit": code, "log": str(log),
            "ausgabe": letzte}


def laufen(wurzel, profil, namen, dateien, immer=False, ordner=None):
    """Wählt, überspringt und führt aus. Ergebnisliste in der Reihenfolge der Namen."""
    ordner = ordner or tempfile.mkdtemp(prefix="checks-")
    merker_datei = merker_pfad(wurzel)
    try:
        merker = json.loads(merker_datei.read_text(encoding="utf-8")) if merker_datei and merker_datei.is_file() else {}
    except (OSError, json.JSONDecodeError):
        merker = {}
    ergebnisse, offen = {}, []
    for name in namen:
        check = profil["checks"].get(name)
        if check is None:
            ergebnisse[name] = {"name": name, "ergebnis": "unbekannt", "grund": "nicht unter ### Checks im Profil"}
            continue
        treffer = passende(dateien, check["muster"])
        if check["muster"] and not treffer:
            ergebnisse[name] = {"name": name, "ergebnis": "übersprungen", "grund": "keine passende Datei"}
            continue
        abdruck = fingerabdruck(wurzel, check, treffer)
        if not immer and merker.get(name) == abdruck:
            ergebnisse[name] = {"name": name, "ergebnis": "schon grün", "grund": "seit dem letzten grünen Lauf unverändert"}
            continue
        offen.append((name, check, abdruck))

    def eins(eintrag):
        name, check, abdruck = eintrag
        return name, abdruck, ausfuehren(name, check, wurzel, ordner)

    gemeinsam = [e for e in offen if not e[1]["allein"]]
    allein = [e for e in offen if e[1]["allein"]]
    fertig = []
    if gemeinsam:
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(gemeinsam)) as pool:
            fertig += list(pool.map(eins, gemeinsam))
    fertig += [eins(e) for e in allein]
    for name, abdruck, ergebnis in fertig:
        ergebnisse[name] = ergebnis
        if ergebnis["ergebnis"] == "grün":
            merker[name] = abdruck
        else:
            merker.pop(name, None)
    if merker_datei and fertig:
        try:
            merker_datei.write_text(json.dumps(merker, indent=2, sort_keys=True), encoding="utf-8")
        except OSError:
            pass
    return [ergebnisse[n] for n in namen]


def exit_code(ergebnisse):
    werte = {e["ergebnis"] for e in ergebnisse}
    if "rot" in werte or "unbekannt" in werte:
        return 1
    return 2 if "fehlt" in werte else 0


def tabelle(ergebnisse):
    zeilen = ["| Check | Dauer | Ergebnis |", "|---|---|---|"]
    for e in ergebnisse:
        dauer = f"{int(e['dauer'] // 60)}:{int(e['dauer'] % 60):02d}" if "dauer" in e else "–"
        text = e["ergebnis"] + (f" – {e['grund']}" if e.get("grund") else "")
        if e["ergebnis"] == "fehlt":
            text += " – Befehl auf diesem Rechner nicht vorhanden"
        zeilen.append(f"| {e['name']} | {dauer} | {text} |")
    for e in ergebnisse:
        if e.get("ausgabe"):
            zeilen += ["", f"{e['name']} ({e['ergebnis']}, Ausgabe {e['log']}):", e["ausgabe"]]
    return "\n".join(zeilen)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Prüfläufe vor dem Commit nach dem Skill-Profil")
    wahl = parser.add_mutually_exclusive_group(required=True)
    wahl.add_argument("--vor-commit", action="store_true", help="die Pre-Commit-Checks des Profils")
    wahl.add_argument("--checks", help="Namen, durch Komma getrennt")
    parser.add_argument("--profil", help="CLAUDE.md (Standard: in der Repo-Wurzel)")
    parser.add_argument("--immer", action="store_true", help="auch Checks, die mit diesem Stand schon grün waren")
    parser.add_argument("--json", action="store_true", help="Ergebnis als JSON")
    args = parser.parse_args(argv)
    try:
        r = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True, check=False)
        if r.returncode:
            raise ProfilFehler("kein git-Repo")
        wurzel = r.stdout.strip()
        profil_datei = Path(args.profil) if args.profil else Path(wurzel) / "CLAUDE.md"
        profil = profil_lesen(profil_datei.read_text(encoding="utf-8"))
        namen = profil["vor_commit"] if args.vor_commit else [n.strip() for n in args.checks.split(",") if n.strip()]
        dateien = geaendert(wurzel)
    except (OSError, ProfilFehler) as exc:
        print(json.dumps({"fehler": str(exc)}, ensure_ascii=False) if args.json else f"Fehler: {exc}")
        return 3
    ergebnisse = laufen(wurzel, profil, namen, dateien, immer=args.immer)
    code = exit_code(ergebnisse)
    if args.json:
        print(json.dumps({"ok": code == 0, "exit": code, "checks": ergebnisse}, ensure_ascii=False, indent=2))
    else:
        print(tabelle(ergebnisse) if ergebnisse else "Keine Pre-Commit-Checks im Profil.")
    return code


if __name__ == "__main__":
    sys.exit(main())
