#!/usr/bin/env python3
"""Katalog des Projekt-Generators prüfen: python3 skills/projekt-anlegen/scripts/validate.py [templates-Ordner]

Prüft, was das Skill-Prüfskript (tools/validate-skills.ps1) nicht prüft: Manifeste gültig, jede Kombination einer
Projektart auflösbar (bekannte Bausteine, keine Zyklen oder Konflikte, Vorlagen vorhanden, keine doppelten
Zieldateien), nur erlaubte Platzhalter, UTF-8 ohne BOM, keine Projektwerte (absolute Pfade, Konten) in Vorlagen.
Exit 0 = alles gut, sonst 1 mit den Befunden.
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auftrag import TEMPLATES, AuftragFehler, manifeste  # noqa: E402
from bausteine import (  # noqa: E402
    ERLAUBTE_PLATZHALTER, PLATZHALTER, auswahl, aufloesen, dateiplan, erlaubt, komponenten, versionen,
)

# Werte, die in einer projektneutralen Vorlage nichts verloren haben
VERBOTEN = [
    (re.compile(r"(?<![\w.])/(?:config|data|home|root|Users)/"), "absoluter Pfad"),
    (re.compile(r"[A-Za-z]:\\\\?(?:Users|Program)"), "Windows-Pfad"),
    (re.compile(r"(?i)herbert|schrotter"), "Name eines Kontos"),
    (re.compile(r"(?i)(?:api[_-]?key|token|password|passwort)\s*[:=]\s*['\"][^'\"{]{4,}"), "Zugangsdaten"),
]
MUSTER_AUFTRAG = {
    "schema_version": 1,
    "project": {"name": "Prüfprojekt", "slug": "pruefprojekt", "package": "pruefprojekt"},
    "delivery": {"github": True},
}


def pruefen(templates=TEMPLATES):
    templates = Path(templates)
    befunde = []
    try:
        arten, katalog, katalog_versionen = manifeste(templates), komponenten(templates), versionen(templates)
    except (OSError, ValueError, KeyError) as exc:
        return [f"Manifeste nicht lesbar: {exc}"]

    for art in arten.values():
        for kombination in art.get("kombinationen", []):
            for github in (False, True):
                auftrag = dict(MUSTER_AUFTRAG, template={"id": art["id"], "version": art["version"]},
                               features=dict(kombination), delivery={"github": github})
                wo = f"{art['id']} {kombination}{' + GitHub' if github else ''}"
                try:
                    ids = auswahl(auftrag, art)
                    dateiplan(aufloesen(ids, katalog), katalog, {k: "x" for k in ERLAUBTE_PLATZHALTER}, templates)
                except (AuftragFehler, KeyError) as exc:
                    befunde += [f"{wo}: {f}" for f in getattr(exc, "fehler", [repr(exc)])]

    for path in sorted(p for p in templates.rglob("*") if p.is_file() and "manifests" not in p.parts):
        rel = path.relative_to(templates).as_posix()
        roh = path.read_bytes()
        if roh.startswith(b"\xef\xbb\xbf"):
            befunde.append(f"{rel}: UTF-8 mit BOM")
        try:
            text = roh.decode("utf-8")
        except UnicodeDecodeError:
            befunde.append(f"{rel}: kein UTF-8")
            continue
        if "\r\n" in text:
            befunde.append(f"{rel}: Zeilenenden CRLF statt LF")
        for key in sorted(k for k in {m.group(1) for m in PLATZHALTER.finditer(text)}
                          if not erlaubt(k, katalog_versionen)):
            befunde.append(f"{rel}: unbekannter Platzhalter {{{{{key}}}}}")
        for muster, art_ in VERBOTEN:
            if muster.search(text):
                befunde.append(f"{rel}: {art_} in einer Vorlage")
    return list(dict.fromkeys(befunde))


def main():
    befunde = pruefen(sys.argv[1] if len(sys.argv) > 1 else TEMPLATES)
    for befund in befunde:
        print(f"FEHLER  {befund}")
    print("Katalog in Ordnung" if not befunde else f"{len(befunde)} Befund(e)")
    return 1 if befunde else 0


if __name__ == "__main__":
    sys.exit(main())
