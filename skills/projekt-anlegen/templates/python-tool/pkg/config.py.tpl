"""Einstellungen aus der Umgebung.

Geheimnisse nie im Code oder im Repo; `.env.example` zeigt die Namen.
"""

import os
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path


class EinstellungsFehler(ValueError):
    """Eine Einstellung fehlt oder ist ungültig."""


@dataclass(frozen=True)
class Einstellungen:
    daten: Path


def laden(umgebung: Mapping[str, str] | None = None) -> Einstellungen:
    umgebung = os.environ if umgebung is None else umgebung
    roh = umgebung.get("{{package_upper}}_DATEN", "daten")
    if not roh.strip():
        raise EinstellungsFehler("{{package_upper}}_DATEN ist leer")
    return Einstellungen(daten=Path(roh))
