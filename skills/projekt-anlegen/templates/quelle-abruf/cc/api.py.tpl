"""Verbindung zum Gerät oder Dienst – ohne Home Assistant, damit sie für sich testbar bleibt.

Beispiel ohne Netz: Diese Datei wird durch die echte Bibliothek des Geräts oder Dienstes ersetzt.
"""


class VerbindungFehler(Exception):
    """Gerät oder Dienst nicht erreichbar."""


class Client:
    """Fragt das Gerät unter `adresse` ab."""

    def __init__(self, adresse: str) -> None:
        self.adresse = adresse

    async def abrufen(self) -> dict[str, str]:
        if not self.adresse.strip():
            raise VerbindungFehler("keine Adresse")
        return {"zustand": "ok"}
