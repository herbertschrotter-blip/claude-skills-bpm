"""Speicher ohne Datenhaltung: der technische Status kommt aus dem laufenden Prozess."""

from .config import Einstellungen


class SpeicherImProzess:
    def status_lesen(self) -> str:
        return "ready"


def speicher_fuer(einstellungen: Einstellungen) -> SpeicherImProzess:
    return SpeicherImProzess()
