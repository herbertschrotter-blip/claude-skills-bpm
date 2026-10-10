"""Integration einrichten und entladen."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant

from .const import CONF_QUELLE

PLATTFORMEN = [Platform.SENSOR]


@dataclass
class Laufzeit:
    """Was die Integration zur Laufzeit braucht (entry.runtime_data)."""

    quelle: str

    def diagnose(self) -> dict[str, Any]:
        return {"quelle": self.quelle}


type EintragMitLaufzeit = ConfigEntry[Laufzeit]


async def async_setup_entry(hass: HomeAssistant, entry: EintragMitLaufzeit) -> bool:
    entry.runtime_data = Laufzeit(quelle=entry.data[CONF_QUELLE])
    await hass.config_entries.async_forward_entry_setups(entry, PLATTFORMEN)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: EintragMitLaufzeit) -> bool:
    return await hass.config_entries.async_unload_platforms(entry, PLATTFORMEN)
