"""Neovolt / Bytewatt battery bridge via the upstream Neovolt integration.

PowerSync does not open a Modbus connection here. The HACS Neovolt integration
owns the Modbus session; this controller discovers its Home Assistant entities
and writes the dispatch controls through HA services.

Sign conventions:
  PowerSync battery_power: positive = discharging, negative = charging
  Neovolt battery_power:  positive = discharging, negative = charging
  PowerSync grid_power:   positive = importing, negative = exporting
  Neovolt grid_power_total follows the same convention.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.helpers import entity_registry as er

_LOGGER = logging.getLogger(__name__)


_READ_ENTITIES: dict[str, tuple[tuple[str, str], ...]] = {
    "battery_power": (
        ("sensor", "combined_battery_power"),
        ("sensor", "battery_power"),
    ),
    "battery_level": (
        ("sensor", "combined_battery_soc"),
        ("sensor", "battery_soc"),
    ),
    "battery_capacity_kwh": (
        ("sensor", "combined_battery_capacity"),
        ("sensor", "battery_capacity"),
    ),
    "load_power": (
        ("sensor", "combined_house_load"),
        ("sensor", "total_house_load"),
    ),
    "solar_power": (
        ("sensor", "combined_pv_power"),
        ("sensor", "pv_total_active_power"),
        ("sensor", "pv_power_total"),
    ),
    "grid_power": (
        ("sensor", "grid_total_active_power"),
        ("sensor", "grid_power_total"),
    ),
    "battery_soh": (
        ("sensor", "combined_battery_soh"),
        ("sensor", "battery_soh"),
    ),
}

_WRITE_ENTITIES: dict[str, tuple[tuple[str, str], ...]] = {
    "dispatch_mode": (("select", "dispatch_mode"),),
    "dispatch_power": (("number", "dispatch_power"),),
    "dispatch_duration": (("number", "dispatch_duration"),),
    "dispatch_charge_soc": (
        ("number", "dispatch_charge_target_soc"),
        ("number", "dispatch_charge_soc"),
    ),
    "dispatch_discharge_soc": (
        ("number", "dispatch_discharge_cutoff_soc"),
        ("number", "dispatch_discharge_soc"),
    ),
    "backup_reserve": (
        ("number", "discharging_cutoff_soc_default"),
        ("number", "discharging_cutoff_soc"),
    ),
    "stop_dispatch_button": (
        ("button", "stop_force_charge_discharge"),
        ("button", "stop_dispatch"),
    ),
}

_CONTROL_REQUIRED = (
    "dispatch_mode",
    "dispatch_power",
    "dispatch_duration",
    "dispatch_charge_soc",
    "dispatch_discharge_soc",
)

_READ_REQUIRED = (
    "battery_power",
    "battery_level",
    "grid_power",
    "load_power",
    "solar_power",
)


class NeovoltBatteryController:
    """Bridge controller for Neovolt entities exposed by the HACS integration."""

    def __init__(
        self,
        hass: Any,
        neovolt_entry_id: str,
        max_charge_kw: float = 5.0,
        max_discharge_kw: float = 5.0,
        min_soc_pct: float = 10.0,
    ) -> None:
        self.hass = hass
        self._neovolt_entry_id = neovolt_entry_id
        self._max_charge_kw = float(max_charge_kw)
        self._max_discharge_kw = float(max_discharge_kw)
        self._min_soc_pct = float(min_soc_pct)
        self._entity_map: dict[str, str] = {}

    def set_min_soc_pct(self, min_soc_pct: float) -> None:
        """Update the discharge cutoff used for force-discharge commands."""
        self._min_soc_pct = float(min_soc_pct)

    async def connect(self) -> bool:
        """Validate that required Neovolt entities exist."""
        self._discover_entities()

        missing = self._missing_keys(_READ_REQUIRED + _CONTROL_REQUIRED)
        if missing:
            missing_ids = [
                self._entity_map.get(key)
                or self._expected_entity_hint(key)
                or key
                for key in missing
            ]
            raise ValueError(f"neovolt_missing_entities:{','.join(missing_ids)}")

        _LOGGER.info(
            "Neovolt entities validated via config entry %s (%d mapped)",
            self._neovolt_entry_id,
            len(self._entity_map),
        )
        return True

    async def disconnect(self) -> None:
        """No persistent connection to close."""
        return None

    def get_status(self) -> dict[str, Any]:
        """Read current Neovolt state and return PowerSync-canonical fields."""
        if not self._entity_map:
            self._discover_entities()

        battery_w = self._read_float("battery_power") or 0.0
        grid_w = self._read_float("grid_power") or 0.0
        solar_w = self._read_float("solar_power") or 0.0
        load_w = self._read_float("load_power") or 0.0

        return {
            "solar_power": max(0.0, solar_w / 1000.0),
            "grid_power": grid_w / 1000.0,
            "battery_power": battery_w / 1000.0,
            "load_power": max(0.0, load_w / 1000.0),
            "battery_level": self._read_float("battery_level") or 0.0,
            "battery_capacity_kwh": self._read_float("battery_capacity_kwh"),
            "battery_soh": self._read_float("battery_soh"),
            "battery_max_charge_power_w": self._max_charge_kw * 1000.0,
            "battery_max_discharge_power_w": self._max_discharge_kw * 1000.0,
        }

    async def force_charge(self, duration_minutes: int, power_w: int | float) -> bool:
        """Force battery to charge via Neovolt dispatch controls."""
        await self._ensure_connected()
        power_kw = self._watts_to_kw(power_w, self._max_charge_kw)
        try:
            await self._set_number("dispatch_power", power_kw)
            await self._set_number("dispatch_duration", int(duration_minutes))
            await self._set_number("dispatch_charge_soc", 100)
            await self._set_select("dispatch_mode", "Force Charge")
        except Exception:
            _LOGGER.exception("Neovolt force_charge failed")
            return False

        _LOGGER.info(
            "Neovolt force_charge: %.1f kW for %d minutes",
            power_kw,
            duration_minutes,
        )
        return True

    async def force_discharge(self, duration_minutes: int, power_w: int | float) -> bool:
        """Force battery to discharge via Neovolt dispatch controls."""
        await self._ensure_connected()
        power_kw = self._watts_to_kw(power_w, self._max_discharge_kw)
        cutoff_soc = max(4, min(100, int(round(self._min_soc_pct))))
        try:
            await self._set_number("dispatch_power", power_kw)
            await self._set_number("dispatch_duration", int(duration_minutes))
            await self._set_number("dispatch_discharge_soc", cutoff_soc)
            await self._set_select("dispatch_mode", "Force Discharge")
        except Exception:
            _LOGGER.exception("Neovolt force_discharge failed")
            return False

        _LOGGER.info(
            "Neovolt force_discharge: %.1f kW for %d minutes, cutoff SOC %d%%",
            power_kw,
            duration_minutes,
            cutoff_soc,
        )
        return True

    async def restore_normal(self) -> bool:
        """Return Neovolt dispatch mode to Normal."""
        await self._ensure_connected()
        try:
            await self._set_select("dispatch_mode", "Normal")
            _LOGGER.info("Neovolt restored to Normal dispatch mode")
            return True
        except Exception:
            _LOGGER.exception("Neovolt restore_normal select failed")

        if self._entity_map.get("stop_dispatch_button"):
            try:
                await self._press_button("stop_dispatch_button")
                _LOGGER.info("Neovolt stop dispatch button pressed as recovery fallback")
                return True
            except Exception:
                _LOGGER.exception("Neovolt stop dispatch fallback failed")
        return False

    async def set_backup_reserve(self, percent: int) -> bool:
        """Set the default discharging cutoff SOC in the Neovolt integration."""
        await self._ensure_connected()
        self._min_soc_pct = float(percent)
        if not self._entity_exists("backup_reserve"):
            _LOGGER.warning("Neovolt backup reserve entity not found")
            return False
        clamped = max(4, min(100, int(percent)))
        await self._set_number("backup_reserve", clamped)
        _LOGGER.info("Neovolt discharging cutoff SOC set to %d%%", clamped)
        return True

    async def get_backup_reserve(self) -> int | None:
        """Read the current default discharging cutoff SOC."""
        await self._ensure_connected()
        reserve = self._read_float("backup_reserve")
        return int(reserve) if reserve is not None else None

    async def set_idle(self) -> bool:
        """Best-effort hold: raise the discharge cutoff to the current SOC."""
        status = self.get_status()
        current_soc = status.get("battery_level")
        if current_soc is None:
            return False
        return await self.set_backup_reserve(int(round(current_soc)))

    def _discover_entities(self) -> None:
        """Populate logical entity map from selected config entry and live states."""
        self._entity_map = {}
        candidates = self._entity_candidates()

        for key, patterns in _READ_ENTITIES.items():
            entity_id = self._resolve_entity_id(candidates, patterns)
            if entity_id:
                self._entity_map[key] = entity_id

        for key, patterns in _WRITE_ENTITIES.items():
            entity_id = self._resolve_entity_id(candidates, patterns)
            if entity_id:
                self._entity_map[key] = entity_id

    def _entity_candidates(self) -> list[tuple[str, str | None, int]]:
        registry = er.async_get(self.hass)
        entries = er.async_entries_for_config_entry(registry, self._neovolt_entry_id)
        candidates: list[tuple[str, str | None, int]] = [
            (entry.entity_id, getattr(entry, "unique_id", None), 0)
            for entry in entries
            if getattr(entry, "entity_id", None)
        ]
        seen = {entity_id for entity_id, _unique_id, _priority in candidates}
        for state in self.hass.states.async_all():
            entity_id = state.entity_id
            if (
                entity_id.startswith(("sensor.", "number.", "select.", "button."))
                and entity_id not in seen
                and ".neovolt_" in entity_id
            ):
                candidates.append((entity_id, None, 1))
                seen.add(entity_id)
        return candidates

    def _resolve_entity_id(
        self,
        candidates: list[tuple[str, str | None, int]],
        patterns: tuple[tuple[str, str], ...],
    ) -> str | None:
        for domain, suffix in patterns:
            domain_prefix = f"{domain}."
            matches: list[tuple[str, int]] = []
            entity_tail = f"_{suffix}"
            unique_tail = f"_{suffix}"
            for entity_id, unique_id, priority in candidates:
                if not entity_id.startswith(domain_prefix):
                    continue
                object_id = entity_id.split(".", 1)[1]
                if (
                    object_id.endswith(entity_tail)
                    or (unique_id and unique_id.endswith(unique_tail))
                ):
                    matches.append((entity_id, priority))
            if not matches:
                continue
            matches = sorted(
                matches,
                key=lambda match: (
                    match[1],
                    0 if self.hass.states.get(match[0]) is not None else 1,
                    len(match[0]),
                    match[0],
                ),
            )
            return matches[0][0]
        return None

    async def _ensure_connected(self) -> None:
        if not self._entity_map:
            await self.connect()

    def _expected_entity_hint(self, key: str) -> str | None:
        patterns = _READ_ENTITIES.get(key) or _WRITE_ENTITIES.get(key)
        if not patterns:
            return None
        domain, suffix = patterns[0]
        return f"{domain}.neovolt_1_{suffix}"

    def _missing_keys(self, keys: tuple[str, ...]) -> list[str]:
        return [
            key for key in keys
            if key not in self._entity_map
            or self.hass.states.get(self._entity_map.get(key, "")) is None
        ]

    def _entity_exists(self, key: str) -> bool:
        entity_id = self._entity_map.get(key)
        return bool(entity_id and self.hass.states.get(entity_id) is not None)

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

    async def _set_number(self, key: str, value: float | int) -> None:
        entity_id = self._entity_map.get(key)
        if not entity_id:
            raise ValueError(f"Neovolt number entity not mapped: {key}")
        await self.hass.services.async_call(
            "number",
            "set_value",
            {"entity_id": entity_id, "value": value},
            blocking=True,
        )

    async def _set_select(self, key: str, option: str) -> None:
        entity_id = self._entity_map.get(key)
        if not entity_id:
            raise ValueError(f"Neovolt select entity not mapped: {key}")
        await self.hass.services.async_call(
            "select",
            "select_option",
            {"entity_id": entity_id, "option": option},
            blocking=True,
        )

    async def _press_button(self, key: str) -> None:
        entity_id = self._entity_map.get(key)
        if not entity_id:
            raise ValueError(f"Neovolt button entity not mapped: {key}")
        await self.hass.services.async_call(
            "button",
            "press",
            {"entity_id": entity_id},
            blocking=True,
        )

    @staticmethod
    def _watts_to_kw(power_w: int | float, default_kw: float) -> float:
        if power_w and power_w > 0:
            return round(float(power_w) / 1000.0, 3)
        return float(default_kw)


class NeovoltFleetBatteryController:
    """Aggregate and control multiple Neovolt battery controllers as one system."""

    def __init__(
        self,
        hass: Any,
        neovolt_entry_ids: list[str],
        max_charge_kw: float = 5.0,
        max_discharge_kw: float = 5.0,
        min_soc_pct: float = 10.0,
    ) -> None:
        if not neovolt_entry_ids:
            raise ValueError("neovolt_missing_entries")

        self._controllers = [
            NeovoltBatteryController(
                hass,
                neovolt_entry_id=entry_id,
                max_charge_kw=max_charge_kw,
                max_discharge_kw=max_discharge_kw,
                min_soc_pct=min_soc_pct,
            )
            for entry_id in neovolt_entry_ids
        ]

    def set_min_soc_pct(self, min_soc_pct: float) -> None:
        """Update the discharge cutoff used for force-discharge commands."""
        for controller in self._controllers:
            controller.set_min_soc_pct(min_soc_pct)

    async def connect(self) -> bool:
        """Validate all configured Neovolt controllers."""
        for controller in self._controllers:
            await controller.connect()
        return True

    async def disconnect(self) -> None:
        """Disconnect all child controllers."""
        for controller in self._controllers:
            await controller.disconnect()

    def get_status(self) -> dict[str, Any]:
        """Read and aggregate current Neovolt fleet state."""
        statuses = [controller.get_status() for controller in self._controllers]
        capacities = [status.get("battery_capacity_kwh") for status in statuses]
        total_capacity = sum(cap for cap in capacities if cap is not None)
        solar_power = sum(status.get("solar_power", 0.0) or 0.0 for status in statuses)
        grid_power = sum(status.get("grid_power", 0.0) or 0.0 for status in statuses)
        battery_power = sum(status.get("battery_power", 0.0) or 0.0 for status in statuses)
        reported_load = sum(status.get("load_power", 0.0) or 0.0 for status in statuses)
        balanced_load = max(0.0, solar_power + grid_power + battery_power)
        load_power = balanced_load if len(statuses) > 1 else reported_load

        return {
            "solar_power": solar_power,
            "grid_power": grid_power,
            "battery_power": battery_power,
            "load_power": load_power,
            "battery_level": self._weighted_average(statuses, "battery_level", capacities),
            "battery_capacity_kwh": total_capacity or None,
            "battery_soh": self._weighted_average(statuses, "battery_soh", capacities),
            "battery_max_charge_power_w": sum(
                status.get("battery_max_charge_power_w", 0.0) or 0.0
                for status in statuses
            ),
            "battery_max_discharge_power_w": sum(
                status.get("battery_max_discharge_power_w", 0.0) or 0.0
                for status in statuses
            ),
        }

    async def force_charge(self, duration_minutes: int, power_w: int | float) -> bool:
        """Force all batteries to charge via their Neovolt dispatch controls."""
        powers = self._split_power_w(power_w, "_max_charge_kw")
        results = [
            await controller.force_charge(duration_minutes, split_power)
            for controller, split_power in zip(self._controllers, powers)
        ]
        return all(results)

    async def force_discharge(self, duration_minutes: int, power_w: int | float) -> bool:
        """Force all batteries to discharge via their Neovolt dispatch controls."""
        powers = self._split_power_w(power_w, "_max_discharge_kw")
        results = [
            await controller.force_discharge(duration_minutes, split_power)
            for controller, split_power in zip(self._controllers, powers)
        ]
        return all(results)

    async def restore_normal(self) -> bool:
        """Return all Neovolt dispatch modes to Normal."""
        results = [await controller.restore_normal() for controller in self._controllers]
        return all(results)

    async def set_backup_reserve(self, percent: int) -> bool:
        """Set the default discharging cutoff SOC on all Neovolt controllers."""
        results = [
            await controller.set_backup_reserve(percent)
            for controller in self._controllers
        ]
        return all(results)

    async def get_backup_reserve(self) -> int | None:
        """Read the lowest configured default discharging cutoff SOC."""
        reserves = [
            await controller.get_backup_reserve()
            for controller in self._controllers
        ]
        known_reserves = [reserve for reserve in reserves if reserve is not None]
        return min(known_reserves) if known_reserves else None

    async def set_idle(self) -> bool:
        """Best-effort hold: raise each inverter's discharge cutoff to its SOC."""
        results = [await controller.set_idle() for controller in self._controllers]
        return all(results)

    def _split_power_w(
        self,
        power_w: int | float,
        limit_attr: str,
    ) -> list[int | float]:
        if not power_w or power_w <= 0:
            return [0 for _controller in self._controllers]

        limits_kw = [
            max(0.0, float(getattr(controller, limit_attr, 0.0)))
            for controller in self._controllers
        ]
        total_kw = sum(limits_kw)
        if total_kw <= 0:
            return [float(power_w) / len(self._controllers) for _controller in self._controllers]

        return [
            float(power_w) * (limit_kw / total_kw)
            for limit_kw in limits_kw
        ]

    @staticmethod
    def _weighted_average(
        statuses: list[dict[str, Any]],
        key: str,
        capacities: list[float | None],
    ) -> float:
        weighted_values = [
            (float(status[key]), float(capacity))
            for status, capacity in zip(statuses, capacities)
            if status.get(key) is not None and capacity is not None and capacity > 0
        ]
        total_capacity = sum(capacity for _value, capacity in weighted_values)
        if total_capacity > 0:
            return sum(value * capacity for value, capacity in weighted_values) / total_capacity

        values = [
            float(status[key])
            for status in statuses
            if status.get(key) is not None
        ]
        return sum(values) / len(values) if values else 0.0
