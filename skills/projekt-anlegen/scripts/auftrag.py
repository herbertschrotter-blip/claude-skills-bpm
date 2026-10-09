"""Erzeugungsauftrag v1 des Projekt-Generators prüfen (nur Standardbibliothek).

Der Auftrag ist ein kurzlebiges JSON, das projekt-anlegen aus den bestätigten Antworten baut
(references/generator.md). Der Generator vertraut ihm nicht blind: Jede Abweichung vom Schema ist ein Fehler,
bevor auch nur eine Datei entsteht. Ablage, GitHub-Owner, Branch- und Push-Policy und Prüfbefehle stehen nie im
Auftrag – die kommen aus dem Skill-Profil bzw. aus den Vorlagen.

    {
      "schema_version": 1,
      "project": {"name": "Beispiel Werkzeug", "slug": "beispiel-werkzeug", "package": "beispiel_werkzeug"},
      "template": {"id": "python-tool", "version": 1},
      "features": {"storage": "sqlite"},
      "delivery": {"github": false}
    }
"""

import json
import keyword
import os
import re
import sys
import unicodedata
from pathlib import Path

SCHEMA_VERSION = 1
TEMPLATES = Path(__file__).resolve().parent.parent / "templates"

_SLUG = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_PACKAGE = re.compile(r"^[a-z][a-z0-9_]*$")
_KEYS = {
    "": {"schema_version", "project", "template", "features", "delivery"},
    "project": {"name", "slug", "package"},
    "template": {"id", "version"},
    "delivery": {"github"},
}


class AuftragFehler(ValueError):
    """Ungültiger Auftrag; `fehler` enthält alle Befunde, nicht nur den ersten."""

    def __init__(self, fehler):
        super().__init__("; ".join(fehler))
        self.fehler = list(fehler)


def manifeste(templates=TEMPLATES):
    """Freigegebene Projektarten: {id: manifest} aus templates/manifests/*.json."""
    result = {}
    for path in sorted((Path(templates) / "manifests").glob("*.json")):
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        result[data["id"]] = data
    return result


def _schluessel(obj, wo, fehler):
    """Nur bekannte Schlüssel; fehlende und zusätzliche sind beide ein Fehler."""
    if not isinstance(obj, dict):
        fehler.append(f"{wo or 'Auftrag'}: muss ein Objekt sein")
        return False
    erlaubt = _KEYS[wo]
    for key in sorted(set(obj) - erlaubt):
        fehler.append(f"{wo + '.' if wo else ''}{key}: unbekanntes Feld")
    for key in sorted(erlaubt - set(obj)):
        fehler.append(f"{wo + '.' if wo else ''}{key}: fehlt")
    return True


def _name(value, fehler):
    if not isinstance(value, str) or not value.strip():
        fehler.append("project.name: muss ein nicht leerer Text sein")
        return
    if len(value) > 80:
        fehler.append("project.name: höchstens 80 Zeichen")
    if any(unicodedata.category(c).startswith("C") for c in value):
        fehler.append("project.name: keine Steuerzeichen")
    if any(s in value for s in ("/", "\\", "..", "{{", "}}", "`", "$(", '"')):
        fehler.append("project.name: keine Pfad-, Platzhalter-, Anführungs- oder Befehlszeichen (/ \\ .. {{ }} ` $( \")")


def pruefen(data, katalog=None):
    """Prüft einen Auftrag (dict) und gibt ihn unverändert zurück; sonst AuftragFehler mit allen Befunden."""
    katalog = manifeste() if katalog is None else katalog
    fehler = []
    if not _schluessel(data, "", fehler):
        raise AuftragFehler(fehler)

    if data.get("schema_version") != SCHEMA_VERSION or isinstance(data.get("schema_version"), bool):
        fehler.append(f"schema_version: nur {SCHEMA_VERSION} wird unterstützt")

    project = data.get("project")
    if project is not None and _schluessel(project, "project", fehler):
        if "name" in project:
            _name(project["name"], fehler)
        slug = project.get("slug")
        if "slug" in project and (not isinstance(slug, str) or len(slug) > 40 or not _SLUG.match(slug)):
            fehler.append("project.slug: nur Kleinbuchstaben, Ziffern und einzelne Bindestriche, höchstens 40 Zeichen")
        package = project.get("package")
        if "package" in project:
            if not isinstance(package, str) or len(package) > 40 or not _PACKAGE.match(package):
                fehler.append("project.package: gültiger Python-Modulname (Kleinbuchstaben, Ziffern, _), höchstens 40")
            elif keyword.iskeyword(package) or package in sys.stdlib_module_names:
                fehler.append(f"project.package: »{package}« ist ein Schlüsselwort oder ein Modul der Standardbibliothek")

    manifest = None
    template = data.get("template")
    if template is not None and _schluessel(template, "template", fehler):
        manifest = katalog.get(template.get("id")) if isinstance(template.get("id"), str) else None
        if "id" in template and manifest is None:
            fehler.append(f"template.id: unbekannt (erlaubt: {', '.join(sorted(katalog)) or 'keine'})")
        version = template.get("version")
        if manifest is not None and (version != manifest["version"] or isinstance(version, bool)):
            fehler.append(f"template.version: {template['id']} gibt es nur in Version {manifest['version']}")

    features = data.get("features")
    if not isinstance(features, dict):
        fehler.append("features: muss ein Objekt sein")
    elif manifest is not None:
        erlaubt = manifest.get("features", {})
        for key in sorted(set(features) - set(erlaubt)):
            fehler.append(f"features.{key}: gibt es bei {manifest['id']} nicht")
        for key, werte in sorted(erlaubt.items()):
            if key not in features:
                fehler.append(f"features.{key}: fehlt (erlaubt: {', '.join(werte)})")
            elif features[key] not in werte:
                fehler.append(f"features.{key}: »{features[key]}« nicht erlaubt (erlaubt: {', '.join(werte)})")
        freigegeben = manifest.get("kombinationen")
        if freigegeben is not None and not any(features == k for k in freigegeben) and not any(
                f.startswith("features.") for f in fehler):
            fehler.append(f"features: diese Kombination ist für {manifest['id']} nicht freigegeben")

    delivery = data.get("delivery")
    if delivery is not None and _schluessel(delivery, "delivery", fehler):
        if "github" in delivery and not isinstance(delivery["github"], bool):
            fehler.append("delivery.github: true oder false")

    if fehler:
        raise AuftragFehler(fehler)
    return data


def laden(path, katalog=None):
    """Liest und prüft eine Auftragsdatei (UTF-8, mit oder ohne BOM)."""
    try:
        with open(path, encoding="utf-8-sig") as fh:
            data = json.load(fh)
    except json.JSONDecodeError as exc:
        raise AuftragFehler([f"kein gültiges JSON (Zeile {exc.lineno}, Spalte {exc.colno}: {exc.msg})"]) from None
    return pruefen(data, katalog)


def zielordner(ablage, slug):
    """Zielordner <ablage>/<slug>: die Ablage muss existieren, das Ziel darf es nicht, und es liegt wirklich darin
    (auch nach Auflösen von Verknüpfungen)."""
    fehler = []
    basis = Path(ablage)
    if not basis.is_dir():
        raise AuftragFehler([f"Ablage {ablage}: kein vorhandener Ordner"])
    basis = basis.resolve()
    ziel = basis / slug
    if os.path.lexists(ziel):
        fehler.append(f"Ziel {ziel}: existiert schon – der Generator überschreibt nie")
    elif ziel.resolve().parent != basis:
        fehler.append(f"Ziel {ziel}: liegt nicht direkt in der Ablage {basis}")
    if fehler:
        raise AuftragFehler(fehler)
    return ziel
