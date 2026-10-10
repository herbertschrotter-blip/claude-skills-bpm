"""Einrichtung über die Oberfläche: die Quelle wählen."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.helpers.selector import EntitySelector

from .const import CONF_QUELLE, DOMAIN


class EinrichtungsDialog(ConfigFlow, domain=DOMAIN):
    """Eine Quelle je Eintrag; dieselbe Quelle nur einmal."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        fehler: dict[str, str] = {}
        if user_input is not None:
            quelle = user_input[CONF_QUELLE]
            await self.async_set_unique_id(quelle)
            self._abort_if_unique_id_configured()
            zustand = self.hass.states.get(quelle)
            if zustand is None:
                fehler["base"] = "quelle_unbekannt"
            else:
                return self.async_create_entry(title=zustand.name, data={CONF_QUELLE: quelle})
        schema = vol.Schema({vol.Required(CONF_QUELLE): EntitySelector()})
        return self.async_show_form(step_id="user", data_schema=schema, errors=fehler)
