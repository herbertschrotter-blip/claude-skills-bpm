"""Laden, Status-Sensor, Ausfall beim Einrichten, Diagnose und Entladen."""

from unittest.mock import patch

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.{{package}}.api import VerbindungFehler
from custom_components.{{package}}.const import CONF_ADRESSE, DOMAIN
from custom_components.{{package}}.diagnostics import (
    async_get_config_entry_diagnostics,
)


def _eintrag(hass: HomeAssistant) -> MockConfigEntry:
    entry = MockConfigEntry(domain=DOMAIN, data={CONF_ADRESSE: "192.0.2.1"}, unique_id="192.0.2.1")
    entry.add_to_hass(hass)
    return entry


async def _geladen(hass: HomeAssistant) -> MockConfigEntry:
    entry = _eintrag(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


async def test_laden_und_entladen(hass: HomeAssistant) -> None:
    entry = await _geladen(hass)
    assert entry.state is ConfigEntryState.LOADED
    entity_id = er.async_get(hass).async_get_entity_id("sensor", DOMAIN, f"{entry.entry_id}_status")
    assert hass.states.get(entity_id).state == "bereit"
    assert await hass.config_entries.async_unload(entry.entry_id)
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_geraet_nicht_erreichbar(hass: HomeAssistant) -> None:
    entry = _eintrag(hass)
    ziel = f"custom_components.{DOMAIN}.api.Client.abrufen"
    with patch(ziel, side_effect=VerbindungFehler("weg")):
        await hass.config_entries.async_setup(entry.entry_id)
        await hass.async_block_till_done()
    assert entry.state is ConfigEntryState.SETUP_RETRY


async def test_diagnose_schwaerzt_adresse(hass: HomeAssistant) -> None:
    entry = await _geladen(hass)
    diagnose = await async_get_config_entry_diagnostics(hass, entry)
    assert diagnose["eintrag"] == {CONF_ADRESSE: "**REDACTED**"}
    assert diagnose["laufzeit"]["daten"] == {"zustand": "ok"}
