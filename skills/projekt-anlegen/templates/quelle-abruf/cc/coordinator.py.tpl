"""Ein gemeinsamer Abruf für alle Entitäten."""

from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import Client, VerbindungFehler
from .const import DOMAIN, INTERVALL

LOGGER = logging.getLogger(__package__)


class Abruf(DataUpdateCoordinator[dict[str, str]]):
    """Holt die Daten im Takt INTERVALL; ein Fehler macht die Entitäten nicht verfügbar."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry, client: Client) -> None:
        super().__init__(
            hass,
            LOGGER,
            config_entry=entry,
            name=DOMAIN,
            update_interval=INTERVALL,
            always_update=False,
        )
        self.client = client

    async def _async_update_data(self) -> dict[str, str]:
        try:
            return await self.client.abrufen()
        except VerbindungFehler as err:
            raise UpdateFailed(str(err)) from err
