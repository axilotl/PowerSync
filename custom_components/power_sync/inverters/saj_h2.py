"""SAJ H2 / HS2 battery bridge via the upstream saj_h2_modbus integration.

PowerSync does not open a second Modbus connection here. Instead it discovers
the entities created by `stanus74/home-assistant-saj-h2-modbus` and controls
them through Home Assistant services.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.helpers import entity_registry as er

_LOGGER = logging.getLogger(__name__)


_SENSOR_KEYS = {
    "battery_level": ("Bat1SOC", "batEnergyPercent"),
    "battery_power": ("batteryPower",),
    "grid_power": ("totalgridPower", "gridPower"),
    "solar_power": ("pvPower",),
    "load_power": ("TotalLoadPower",),
    "battery_temperature": ("BatTemp", "Bat1Temperature"),
    "app_mode": ("AppMode",),
    "battery_max_charge_power_w": ("BatChargePower", "GridChargePower"),
    "battery_max_discharge_power_w": ("BatDischargePower", "GridDischargePower"),
}

_NUMBER_KEYS = {
    "charge_power": "passive_bat_charge_power",
    "discharge_power": "passive_bat_discharge_power",
    "export_limit": "export_limit",
}

_SWITCH_KEYS = {
    "charge_switch": "passive_charge_control",
    "discharge_switch": "passive_discharge_control",
}


class SajH2BatteryController:
    """Bridge controller for SAJ H2 entities exposed by saj_h2_modbus."""

    def __init__(
        self,
        hass: Any,
        saj_entry_id: str,
        battery_capacity_kwh: float = 10.0,
    ) -> None:
        self.hass = hass
        self._saj_entry_id = saj_entry_id
        self._battery_capacity_kwh = float(battery_capacity_kwh)
        self._entity_map: dict[str, str] = {}

    async def connect(self) -> bool:
        """Validate that the required SAJ entities exist."""
        self._discover_entities()
        required = (
            "battery_level",
            "battery_power",
            "grid_power",
            "solar_power",
            "load_power",
            "charge_power",
            "discharge_power",
            "charge_switch",
            "discharge_switch",
        )
        missing = [key for key in required if key not in self._entity_map]
        if missing:
            raise ValueError(f"saj_missing_entities:{','.join(missing)}")
        _LOGGER.info(
            "SAJ H2 entities validated via config entry %s (%d mapped)",
            self._saj_entry_id,
            len(self._entity_map),
        )
        return True

    def _discover_entities(self) -> None:
        """Discover entity IDs from the upstream config entry."""
        registry = er.async_get(self.hass)
        entries = er.async_entries_for_config_entry(registry, self._saj_entry_id)

        by_uid = {
            reg_entry.unique_id: reg_entry.entity_id
            for reg_entry in entries
            if reg_entry.unique_id and reg_entry.entity_id
        }

        for target, keys in _SENSOR_KEYS.items():
            if target in self._entity_map:
                continue
            for key in keys:
                regular = self._find_uid_suffix(by_uid, f"_{key}", exclude=f"_fast_{key}")
                fast = self._find_uid_suffix(by_uid, f"_fast_{key}")
                chosen = regular or fast
                if chosen:
                    self._entity_map[target] = chosen
                    break

        for target, key in _NUMBER_KEYS.items():
            if target not in self._entity_map:
                entity_id = self._find_uid_suffix(by_uid, f"_{key}_input")
                if entity_id:
                    self._entity_map[target] = entity_id

        for target, suffix in _SWITCH_KEYS.items():
            if target not in self._entity_map:
                entity_id = self._find_uid_suffix(by_uid, suffix)
                if entity_id:
                    self._entity_map[target] = entity_id

    @staticmethod
    def _find_uid_suffix(
        uid_map: dict[str, str],
        suffix: str,
        exclude: str | None = None,
    ) -> str | None:
        for unique_id, entity_id in uid_map.items():
            if exclude and unique_id.endswith(exclude):
                continue
            if unique_id.endswith(suffix):
                return entity_id
        return None

    def get_status(self) -> dict[str, Any]:
        """Read current SAJ state and return PowerSync-canonical fields."""
        return {
            "battery_level": self._read_float("battery_level") or 0.0,
            "battery_power": (self._read_float("battery_power") or 0.0) / 1000.0,
            "grid_power": (self._read_float("grid_power") or 0.0) / 1000.0,
            "solar_power": max(0.0, (self._read_float("solar_power") or 0.0) / 1000.0),
            "load_power": max(0.0, (self._read_float("load_power") or 0.0) / 1000.0),
            "battery_temperature": self._read_float("battery_temperature"),
            "app_mode": self._read_float("app_mode"),
            "battery_capacity_kwh": self._battery_capacity_kwh,
            "battery_max_charge_power_w": self._read_float("battery_max_charge_power_w"),
            "battery_max_discharge_power_w": self._read_float("battery_max_discharge_power_w"),
        }

    async def force_charge(self, duration_minutes: int, power_w: int) -> bool:
        """Enable SAJ passive charge mode."""
        pct = self._power_to_scaled_percent(
            requested_w=power_w,
            max_w=self._read_float("battery_max_charge_power_w"),
        )
        await self._set_number("charge_power", pct)
        await self._turn_off("discharge_switch")
        await self._turn_on("charge_switch")
        _LOGGER.info("SAJ H2 passive charge enabled at %d/1000", pct)
        return True

    async def force_discharge(self, duration_minutes: int, power_w: int) -> bool:
        """Enable SAJ passive discharge mode."""
        pct = self._power_to_scaled_percent(
            requested_w=power_w,
            max_w=self._read_float("battery_max_discharge_power_w"),
        )
        await self._set_number("discharge_power", pct)
        await self._turn_off("charge_switch")
        await self._turn_on("discharge_switch")
        _LOGGER.info("SAJ H2 passive discharge enabled at %d/1000", pct)
        return True

    async def restore_normal(self) -> bool:
        """Disable passive charge/discharge."""
        await self._turn_off("charge_switch")
        await self._turn_off("discharge_switch")
        _LOGGER.info("SAJ H2 restored to normal operation")
        return True

    async def disconnect(self) -> None:
        """No persistent connection to close."""
        return None

    def _power_to_scaled_percent(self, requested_w: int | float, max_w: float | None) -> int:
        """Convert requested watts to SAJ's 0-1000 scale."""
        if requested_w and requested_w > 0 and max_w and max_w > 0:
            return max(0, min(1000, int(round((requested_w / max_w) * 1000))))
        return 1000

    def _read_float(self, key: str) -> float | None:
        entity_id = self._entity_map.get(key)
        if not entity_id:
            return None
        state = self.hass.states.get(entity_id)
        if not state or state.state in ("unavailable", "unknown", ""):
            return None
        try:
            return float(state.state)
        except (TypeError, ValueError):
            return None

    async def _set_number(self, key: str, value: float) -> None:
        entity_id = self._entity_map.get(key)
        if not entity_id:
            raise ValueError(f"Missing SAJ number entity for {key}")
        await self.hass.services.async_call(
            "number",
            "set_value",
            {"entity_id": entity_id, "value": value},
            blocking=True,
        )

    async def _turn_on(self, key: str) -> None:
        entity_id = self._entity_map.get(key)
        if entity_id:
            await self.hass.services.async_call(
                "switch",
                "turn_on",
                {"entity_id": entity_id},
                blocking=True,
            )

    async def _turn_off(self, key: str) -> None:
        entity_id = self._entity_map.get(key)
        if entity_id:
            await self.hass.services.async_call(
                "switch",
                "turn_off",
                {"entity_id": entity_id},
                blocking=True,
            )
