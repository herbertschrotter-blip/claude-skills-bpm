"""Laden, Status-Sensor, Ausfall der Quelle, Diagnose und Entladen."""

from homeassistant.config_entries import ConfigEntryState
from homeassistant.core import HomeAssistant
from homeassistant.helpers import entity_registry as er
from pytest_homeassistant_custom_component.common import MockConfigEntry

from custom_components.{{package}}.const import CONF_QUELLE, DOMAIN
from custom_components.{{package}}.diagnostics import (
    async_get_config_entry_diagnostics,
)


async def _eintrag(hass: HomeAssistant) -> MockConfigEntry:
    hass.states.async_set("sensor.quelle", "5")
    entry = MockConfigEntry(
        domain=DOMAIN, data={CONF_QUELLE: "sensor.quelle"}, unique_id="sensor.quelle"
    )
    entry.add_to_hass(hass)
    assert await hass.config_entries.async_setup(entry.entry_id)
    await hass.async_block_till_done()
    return entry


def _status(hass: HomeAssistant, entry: MockConfigEntry) -> str:
    entity_id = er.async_get(hass).async_get_entity_id("sensor", DOMAIN, f"{entry.entry_id}_status")
    return hass.states.get(entity_id).state


async def test_laden_und_entladen(hass: HomeAssistant) -> None:
    entry = await _eintrag(hass)
    assert entry.state is ConfigEntryState.LOADED
    assert _status(hass, entry) == "bereit"
    assert await hass.config_entries.async_unload(entry.entry_id)
    assert entry.state is ConfigEntryState.NOT_LOADED


async def test_quelle_faellt_aus(hass: HomeAssistant) -> None:
    entry = await _eintrag(hass)
    hass.states.async_set("sensor.quelle", "unavailable")
    await hass.async_block_till_done()
    assert _status(hass, entry) == "quelle_fehlt"
    hass.states.async_set("sensor.quelle", "6")
    await hass.async_block_till_done()
    assert _status(hass, entry) == "bereit"


async def test_diagnose(hass: HomeAssistant) -> None:
    entry = await _eintrag(hass)
    diagnose = await async_get_config_entry_diagnostics(hass, entry)
    assert diagnose["laufzeit"] == {"quelle": "sensor.quelle"}
