"""Einrichtung über die Oberfläche: Adresse eingeben, Verbindung vor dem Anlegen prüfen."""

from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant.config_entries import ConfigFlow, ConfigFlowResult

from .api import Client, VerbindungFehler
from .const import CONF_ADRESSE, DOMAIN


class EinrichtungsDialog(ConfigFlow, domain=DOMAIN):
    """Ein Gerät je Eintrag; dieselbe Adresse nur einmal."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        fehler: dict[str, str] = {}
        if user_input is not None:
            adresse = user_input[CONF_ADRESSE].strip()
            await self.async_set_unique_id(adresse)
            self._abort_if_unique_id_configured()
            try:
                await Client(adresse).abrufen()
            except VerbindungFehler:
                fehler["base"] = "cannot_connect"
            else:
                return self.async_create_entry(title=adresse, data={CONF_ADRESSE: adresse})
        schema = vol.Schema({vol.Required(CONF_ADRESSE): str})
        return self.async_show_form(step_id="user", data_schema=schema, errors=fehler)
