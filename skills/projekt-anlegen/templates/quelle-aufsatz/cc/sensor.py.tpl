"""Technischer Status-Sensor: zeigt, ob die Quelle verfügbar ist."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import Event, EventStateChangedData, HomeAssistant, callback
from homeassistant.helpers.device import async_entity_id_to_device
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.event import async_track_state_change_event

from . import EintragMitLaufzeit
from .logik.status import ZUSTAENDE, status


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EintragMitLaufzeit,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    async_add_entities([StatusSensor(hass, entry)])


class StatusSensor(SensorEntity):
    """Folgt der Quelle ereignisgesteuert, ohne Abfragetakt; hängt am Gerät der Quelle."""

    _attr_has_entity_name = True
    _attr_translation_key = "status"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = list(ZUSTAENDE)
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_should_poll = False

    def __init__(self, hass: HomeAssistant, entry: EintragMitLaufzeit) -> None:
        self._quelle = entry.runtime_data.quelle
        self._attr_unique_id = f"{entry.entry_id}_status"
        self.device_entry = async_entity_id_to_device(hass, self._quelle)
        self._lesen(hass)

    def _lesen(self, hass: HomeAssistant) -> None:
        zustand = hass.states.get(self._quelle)
        self._attr_native_value = status(zustand.state if zustand else None)

    async def async_added_to_hass(self) -> None:
        self.async_on_remove(
            async_track_state_change_event(self.hass, [self._quelle], self._geaendert)
        )

    @callback
    def _geaendert(self, event: Event[EventStateChangedData]) -> None:
        self._lesen(self.hass)
        self.async_write_ha_state()
