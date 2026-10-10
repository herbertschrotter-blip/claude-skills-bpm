"""Anwendungsschicht: kennt den Speicher nur über seine Schnittstelle."""

from typing import Protocol


class StatusSpeicher(Protocol):
    def status_lesen(self) -> str: ...


class StatusDienst:
    def __init__(self, speicher: StatusSpeicher) -> None:
        self._speicher = speicher

    def ausfuehren(self) -> dict[str, str]:
        return {"status": self._speicher.status_lesen()}
