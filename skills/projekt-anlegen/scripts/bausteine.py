"""Bausteine eines geprüften Auftrags auflösen und den Dateiplan bilden (nur Standardbibliothek).

Der Generator kennt keine Stack-Sonderfälle. Was ein Projekt enthält, steht in den Manifesten unter
templates/manifests/: die Projektart (<id>.json) nennt ihre Grundbausteine, die Bausteine je Feature und je
Auslieferung; jeder Baustein (components/<id>.json) nennt, was er voraussetzt, womit er sich nicht verträgt und
welche Vorlagen er wohin schreibt. Platzhalter haben die Form {{name}} und kommen nur aus einer festen Liste.
"""

import json
import re
from pathlib import Path, PurePosixPath

from auftrag import TEMPLATES, AuftragFehler

PLATZHALTER = re.compile(r"\{\{\s*([A-Za-z_][A-Za-z0-9_]*)\s*\}\}")
ERLAUBTE_PLATZHALTER = {"name", "slug", "package", "storage", "github"}


def komponenten(templates=TEMPLATES):
    """Alle Bausteine: {id: manifest} aus templates/manifests/components/*.json."""
    result = {}
    for path in sorted((Path(templates) / "manifests" / "components").glob("*.json")):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        result[data["id"]] = data
    return result


def werte(auftrag):
    """Platzhalterwerte aus dem Auftrag (nur Texte, keine Pfade aus Nutzereingaben)."""
    project = auftrag["project"]
    return {
        "name": project["name"],
        "slug": project["slug"],
        "package": project["package"],
        "storage": auftrag["features"].get("storage", "none"),
        "github": "true" if auftrag["delivery"]["github"] else "false",
    }


def ersetzen(text, werte_, wo="Vorlage"):
    """Ersetzt {{name}}; unbekannte Platzhalter sind ein Fehler, nicht ein stilles Leerfeld."""
    fehler = []

    def eins(match):
        key = match.group(1)
        if key not in ERLAUBTE_PLATZHALTER or key not in werte_:
            fehler.append(f"{wo}: unbekannter Platzhalter {{{{{key}}}}}")
            return match.group(0)
        return str(werte_[key])

    result = PLATZHALTER.sub(eins, text)
    if fehler:
        raise AuftragFehler(fehler)
    return result


def auswahl(auftrag, manifest):
    """Bausteine, die der Auftrag verlangt: Grundbausteine, je Feature, je Auslieferung."""
    ids = list(manifest.get("components", []))
    for key, wert in auftrag["features"].items():
        ids += manifest["features"][key][wert]
    if auftrag["delivery"]["github"]:
        ids += manifest.get("delivery", {}).get("github", [])
    return list(dict.fromkeys(ids))


def aufloesen(ids, katalog):
    """Abhängigkeiten transitiv auflösen; Reihenfolge: Voraussetzungen zuerst. Unbekannte Bausteine, Zyklen und
    Konflikte sind Fehler."""
    fehler, reihenfolge, zustand = [], [], {}

    def besuchen(cid, pfad):
        if cid not in katalog:
            fehler.append(f"Baustein {cid}: unbekannt" + (f" (verlangt von {pfad[-1]})" if pfad else ""))
            return
        if zustand.get(cid) == "fertig":
            return
        if zustand.get(cid) == "offen":
            fehler.append("Zyklus: " + " → ".join(pfad[pfad.index(cid):] + [cid]))
            return
        zustand[cid] = "offen"
        for dep in katalog[cid].get("requires", []):
            besuchen(dep, pfad + [cid])
        zustand[cid] = "fertig"
        reihenfolge.append(cid)

    for cid in ids:
        besuchen(cid, [])
    gewaehlt = set(reihenfolge)
    for cid in reihenfolge:
        for anderer in katalog[cid].get("conflicts", []):
            if anderer in gewaehlt and cid < anderer:
                fehler.append(f"Konflikt: {cid} verträgt sich nicht mit {anderer}")
    if fehler:
        raise AuftragFehler(list(dict.fromkeys(fehler)))
    return reihenfolge


def _ziel_pruefen(ziel, wo):
    """Ziel relativ, ohne .. und ohne Laufwerk; Schreibweise mit / auf allen Plattformen."""
    pfad = PurePosixPath(ziel)
    if not ziel or pfad.is_absolute() or ":" in ziel or "\\" in ziel or ".." in pfad.parts:
        raise AuftragFehler([f"{wo}: Ziel »{ziel}« muss ein relativer Pfad im Projekt sein"])
    return str(pfad)


def dateiplan(reihenfolge, katalog, werte_, templates=TEMPLATES):
    """[(Quelle, Ziel relativ)] in Bausteinreihenfolge. Zwei Bausteine, die dieselbe Datei schreiben, sind ein Fehler –
    gemeinsame Dateien entstehen über einen eigenen Renderer, nie durch Zusammenmischen."""
    fehler, plan, besitzer = [], [], {}
    basis = Path(templates)
    for cid in reihenfolge:
        for eintrag in katalog[cid].get("files", []):
            wo = f"Baustein {cid}"
            try:
                quelle_rel = _ziel_pruefen(eintrag["source"], wo + " (Quelle)")
                ziel = _ziel_pruefen(ersetzen(eintrag["target"], werte_, wo), wo)
            except AuftragFehler as exc:
                fehler += exc.fehler
                continue
            quelle = basis / quelle_rel
            if not quelle.is_file():
                fehler.append(f"{wo}: Vorlage {quelle_rel} fehlt")
            if ziel.lower() in besitzer:
                fehler.append(f"Datei {ziel}: schreiben {besitzer[ziel.lower()]} und {cid}")
                continue
            besitzer[ziel.lower()] = cid
            plan.append((quelle, ziel))
    if fehler:
        raise AuftragFehler(fehler)
    return plan
