#!/usr/bin/env python3
"""Projekt-Generator von projekt-anlegen (nur Standardbibliothek): Erzeugungsauftrag → Projektdateien.

Ablauf und Grenzen: references/generator.md. Dieses Modul erzeugt die Dateien eines geprüften Auftrags in einen
leeren Ordner (Prepare). Prüfen, Veröffentlichen und Rückbau kommen darüber (Verify & Publish).
"""

import json
import tomllib
from pathlib import Path

from auftrag import TEMPLATES, AuftragFehler, manifeste, pruefen
from bausteine import auswahl, aufloesen, dateiplan, ersetzen, komponenten, versionen, werte

GENERATOR_VERSION = "1.0.0"
HERKUNFT = ".projekt-anlegen.json"


def _syntax(ziel, text):
    """Strukturierte Dateien nach dem Ersetzen prüfen: ein Platzhalterwert darf sie nie unlesbar machen."""
    try:
        if ziel.endswith(".toml"):
            tomllib.loads(text)
        elif ziel.endswith(".json"):
            json.loads(text)
    except (tomllib.TOMLDecodeError, json.JSONDecodeError) as exc:
        raise AuftragFehler([f"{ziel}: nach dem Ersetzen ungültig ({exc})"]) from None


def herkunft(auftrag, reihenfolge):
    """Inhalt von .projekt-anlegen.json: nur Herkunft, ohne Datum – gleicher Auftrag, gleiche Datei."""
    return {
        "schema_version": 1,
        "generator": {"name": "projekt-anlegen", "version": GENERATOR_VERSION},
        "template": dict(auftrag["template"]),
        "components": list(reihenfolge),
    }


def erzeugen(auftrag, ordner, templates=TEMPLATES):
    """Schreibt das Projekt in `ordner` (muss existieren und leer sein); gibt die Liste der Dateien zurück."""
    templates = Path(templates)
    arten = manifeste(templates)
    pruefen(auftrag, arten)
    katalog = komponenten(templates)
    reihenfolge = aufloesen(auswahl(auftrag, arten[auftrag["template"]["id"]]), katalog)
    platzhalter = werte(auftrag, versionen(templates))
    plan = dateiplan(reihenfolge, katalog, platzhalter, templates)

    ordner = Path(ordner)
    if not ordner.is_dir() or any(ordner.iterdir()):
        raise AuftragFehler([f"{ordner}: muss ein vorhandener, leerer Ordner sein"])

    inhalte = []
    for quelle, ziel in plan:
        text = ersetzen(quelle.read_text(encoding="utf-8"), platzhalter, quelle.relative_to(templates).as_posix())
        _syntax(ziel, text)
        inhalte.append((ziel, text))
    inhalte.append((HERKUNFT, json.dumps(herkunft(auftrag, reihenfolge), ensure_ascii=False, indent=2) + "\n"))

    for ziel, text in inhalte:  # erst alles rendern, dann schreiben: ein Fehler hinterlässt keine halben Dateien
        pfad = ordner / ziel
        pfad.parent.mkdir(parents=True, exist_ok=True)
        with open(pfad, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    return [ziel for ziel, _ in inhalte]
