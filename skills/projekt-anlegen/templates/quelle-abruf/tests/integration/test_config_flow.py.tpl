"""Einrichtungsdialog: Eintrag anlegen, Adresse nur einmal, keine Verbindung."""

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.{{package}}.const import CONF_ADRESSE, DOMAIN


async def _dialog(hass: HomeAssistant, adresse: str):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    return await hass.config_entries.flow.async_configure(
        result["flow_id"], {CONF_ADRESSE: adresse}
    )


async def test_eintrag_wird_angelegt(hass: HomeAssistant) -> None:
    result = await _dialog(hass, "192.0.2.1")
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {CONF_ADRESSE: "192.0.2.1"}


async def test_adresse_nur_einmal(hass: HomeAssistant) -> None:
    await _dialog(hass, "192.0.2.1")
    result = await _dialog(hass, "192.0.2.1")
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_keine_verbindung(hass: HomeAssistant) -> None:
    result = await _dialog(hass, " ")
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "cannot_connect"}
