"""Diagnose-Download: Einstellungen und Laufzeit, vertrauliche Werte geschwärzt."""

from __future__ import annotations

from typing import Any

from homeassistant.components.diagnostics import async_redact_data
from homeassistant.core import HomeAssistant

from . import EintragMitLaufzeit

VERTRAULICH = {"adresse", "passwort", "token"}


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: EintragMitLaufzeit
) -> dict[str, Any]:
    """Was beim Fehlersuchen hilft, ohne Zugangsdaten."""
    return {
        "eintrag": async_redact_data(dict(entry.data), VERTRAULICH),
        "optionen": async_redact_data(dict(entry.options), VERTRAULICH),
        "laufzeit": async_redact_data(entry.runtime_data.diagnose(), VERTRAULICH),
    }
