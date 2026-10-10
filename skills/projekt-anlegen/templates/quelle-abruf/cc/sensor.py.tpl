"""Technischer Status-Sensor: zeigt, ob der letzte Abruf gültige Daten geliefert hat."""

from __future__ import annotations

from homeassistant.components.sensor import SensorDeviceClass, SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from . import EintragMitLaufzeit
from .const import DOMAIN
from .coordinator import Abruf
from .logik.status import ZUSTAENDE, status


async def async_setup_entry(
    hass: HomeAssistant,
    entry: EintragMitLaufzeit,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    async_add_entities([StatusSensor(entry)])


class StatusSensor(CoordinatorEntity[Abruf], SensorEntity):
    """Wert aus dem gemeinsamen Abruf; nicht verfügbar, wenn der Abruf scheitert."""

    _attr_has_entity_name = True
    _attr_translation_key = "status"
    _attr_device_class = SensorDeviceClass.ENUM
    _attr_options = list(ZUSTAENDE)
    _attr_entity_category = EntityCategory.DIAGNOSTIC

    def __init__(self, entry: EintragMitLaufzeit) -> None:
        super().__init__(entry.runtime_data.abruf)
        self._attr_unique_id = f"{entry.entry_id}_status"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)}, name=entry.title
        )

    @property
    def native_value(self) -> str:
        return status(self.coordinator.data.get("zustand"))
