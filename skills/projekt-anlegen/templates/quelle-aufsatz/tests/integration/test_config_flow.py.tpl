"""Einrichtungsdialog: Eintrag anlegen, Quelle nur einmal, unbekannte Quelle."""

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResultType

from custom_components.{{package}}.const import CONF_QUELLE, DOMAIN


async def _dialog(hass: HomeAssistant, quelle: str):
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )
    assert result["type"] is FlowResultType.FORM
    return await hass.config_entries.flow.async_configure(result["flow_id"], {CONF_QUELLE: quelle})


async def test_eintrag_wird_angelegt(hass: HomeAssistant) -> None:
    hass.states.async_set("sensor.quelle", "5")
    result = await _dialog(hass, "sensor.quelle")
    assert result["type"] is FlowResultType.CREATE_ENTRY
    assert result["data"] == {CONF_QUELLE: "sensor.quelle"}


async def test_quelle_nur_einmal(hass: HomeAssistant) -> None:
    hass.states.async_set("sensor.quelle", "5")
    await _dialog(hass, "sensor.quelle")
    result = await _dialog(hass, "sensor.quelle")
    assert result["type"] is FlowResultType.ABORT
    assert result["reason"] == "already_configured"


async def test_unbekannte_quelle(hass: HomeAssistant) -> None:
    result = await _dialog(hass, "sensor.gibt_es_nicht")
    assert result["type"] is FlowResultType.FORM
    assert result["errors"] == {"base": "quelle_unbekannt"}
