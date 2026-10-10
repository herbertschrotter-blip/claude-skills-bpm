"""Technischer Status – Beispiel für Fachlogik ohne Home Assistant.

Fehlt die Quelle oder ist sie nicht verfügbar, meldet die Integration das als eigenen Zustand,
statt auf alten Daten weiterzuarbeiten.
"""

BEREIT = "bereit"
QUELLE_FEHLT = "quelle_fehlt"
ZUSTAENDE = (BEREIT, QUELLE_FEHLT)

NICHT_VERFUEGBAR = {None, "", "unavailable", "unknown"}


def status(zustand: str | None) -> str:
    """Status aus dem Zustand der Quelle: bereit oder quelle_fehlt."""
    return QUELLE_FEHLT if zustand in NICHT_VERFUEGBAR else BEREIT
