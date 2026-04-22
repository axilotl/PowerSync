"""Solax hybrid battery controller using wills106/homeassistant-solax-modbus entities.

Requires the solax_modbus integration (HACS) to be installed and running.
PowerSync reads sensor states and writes number/select entities via HA service calls
- no direct Modbus connection is opened here (avoids the one-master-at-a-time
restriction of the Solax PocketWiFi dongle).

Supported: Gen4, Gen5, Gen6 Hybrid and AC Retro-Fit (X1 and X3 families).
Gen2/Gen3 use a different control model (Force Time Use windows) and will fail
at connect() with a clear missing-entity error.

Sign conventions (PowerSync internal):
  grid_power_kw   : positive = importing, negative = exporting
  battery_power_kw: positive = discharging, negative = charging
  solar_power_kw  : always >= 0

Solax entity conventions (wills106):
  sensor.*_measured_power      : positive = importing, negative = exporting
  sensor.*_battery_power_charge: positive = charging (OPPOSITE -> negate)
"""

import logging
from typing import Any

from homeassistant.helpers import entity_registry as er

_LOGGER = logging.getLogger(__name__)


# wills106 entity suffixes keyed by role. Some installs expose inverter-prefixed
# variants, and older firmware/plugin combinations may still surface
# `manual_mode` rather than `manual_mode_select`.
_READ_ENTITIES = {
    "battery_level": ("battery_capacity",),            # %
    "battery_power_raw": ("battery_power_charge",),    # W, +charge/-discharge
    "grid_power": ("measured_power",),                 # W, +import/-export
    "pv1_power": ("pv_power_1",),                      # W
    "pv2_power": ("pv_power_2",),                      # W
    "load_power": ("inverter_power",),                 # W
    "battery_temp": ("battery_temperature",),          # C
}

_WRITE_ENTITIES = {
    "charger_use_mode": (
        "charger_use_mode",
        "inverter_charger_use_mode",
    ),
    "manual_mode_select": (
        "manual_mode_select",
        "manual_mode",
        "inverter_manual_mode_select",
        "inverter_manual_mode",
    ),
    "manual_mode_control": (
        "manual_mode_control",
        "inverter_manual_mode_control",
    ),
    "charge_current": ("battery_charge_max_current",),         # number, A
    "discharge_current": ("battery_discharge_max_current",),   # number, A
    "backup_reserve": ("battery_minimum_capacity",),           # number, %
    "export_limit": ("export_control_user_limit",),            # number, W
}


# Expected select options (wills106 label strings for Gen4/Gen5/Gen6)
_MODE_SELF_USE = "Self Use Mode"
_MODE_FEEDIN = "Feedin Priority Mode"
_MODE_BACKUP = "Back Up Mode"
_MODE_MANUAL = "Manual Mode"
_MODE_SMART = "Smart Schedule"

_MANUAL_STOP = "Stop Charge and Discharge"
_MANUAL_CHARGE = "Force Charge"
_MANUAL_DISCHARGE = "Force Discharge"
_MANUAL_CONTROL_ON = "On"
_MANUAL_CONTROL_OFF = "Off"


# PowerSync operation-mode -> Solax charger_use_mode option
_OP_MODE_MAP = {
    "self_consumption": _MODE_SELF_USE,
    "autonomous": _MODE_SMART,
    "backup": _MODE_BACKUP,
    "feed_in": _MODE_FEEDIN,
}


class SolaxBatteryController:
    """Battery controller for Solax Hybrid via homeassistant-solax-modbus."""

    def __init__(
        self,
        hass: Any,
        entity_prefix: str = "solax",
        solax_entry_id: str | None = None,
        battery_nominal_v: float = 51.2,
        max_charge_current_a: float = 25.0,
        max_discharge_current_a: float = 25.0,
    ) -> None:
        self.hass = hass
        self._prefix = entity_prefix.strip()
        self._solax_entry_id = (solax_entry_id or "").strip()
        self._nominal_v = battery_nominal_v
        self._max_charge_a = max_charge_current_a
        self._max_discharge_a = max_discharge_current_a
        self._timer_cancel = None
        self._entity_map: dict[str, str] = {}

    # -- Entity ID helpers -------------------------------------------------

    def _sensor(self, suffix: str) -> str:
        return f"sensor.{self._prefix}_{suffix}"

    def _number(self, suffix: str) -> str:
        return f"number.{self._prefix}_{suffix}"

    def _select(self, suffix: str) -> str:
        return f"select.{self._prefix}_{suffix}"

    @staticmethod
    def _find_entity_by_suffix(
        entity_ids: list[str],
        domain: str,
        suffixes: tuple[str, ...],
    ) -> str | None:
        domain_prefix = f"{domain}."
        for suffix in suffixes:
            tail = f"_{suffix}"
            for entity_id in entity_ids:
                if entity_id.startswith(domain_prefix) and entity_id.endswith(tail):
                    return entity_id
        return None

    # -- Prefix discovery --------------------------------------------------

    @staticmethod
    def discover_prefixes(hass: Any) -> list[str]:
        """Scan HA states for likely wills106 hybrid inverter prefixes."""
        batt_suffix = f"_{_READ_ENTITIES['battery_level'][0]}"
        mode_suffixes = [f"_{v}" for v in _WRITE_ENTITIES["charger_use_mode"]]

        mode_prefixes = set()
        for state in hass.states.async_all("select"):
            eid = state.entity_id
            for mode_suffix in mode_suffixes:
                if eid.endswith(mode_suffix):
                    prefix = eid[len("select."):-len(mode_suffix)]
                    if prefix:
                        mode_prefixes.add(prefix)
                    break

        prefixes = []
        for prefix in mode_prefixes:
            if hass.states.get(f"sensor.{prefix}{batt_suffix}") is not None:
                prefixes.append(prefix)
        return sorted(prefixes)

    # -- Connect / validate ------------------------------------------------

    async def connect(self) -> bool:
        """Validate that required Solax entities exist."""
        self._discover_entities()

        required = (
            "battery_level",
            "battery_power_raw",
            "grid_power",
            "charger_use_mode",
            "manual_mode_select",
            "charge_current",
            "discharge_current",
            "backup_reserve",
        )
        missing = [
            key for key in required
            if key not in self._entity_map
            or self.hass.states.get(self._entity_map.get(key, "")) is None
        ]
        if missing:
            missing_ids = [
                self._entity_map.get(key)
                or self._expected_entity_hint(key)
                or key
                for key in missing
            ]
            raise ValueError(f"solax_missing_entities:{','.join(missing_ids)}")

        _LOGGER.info(
            "Solax entities validated (%s, %d mapped)",
            (
                f"config_entry={self._solax_entry_id}"
                if self._solax_entry_id
                else f"prefix={self._prefix}"
            ),
            len(self._entity_map),
        )
        return True

    # -- Status ------------------------------------------------------------

    def get_status(self) -> dict[str, Any]:
        """Read current inverter state and return PowerSync-canonical dict."""
        soc = self._read_float("battery_level") or 0.0
        bat_w_raw = self._read_float("battery_power_raw") or 0.0
        grid_w = self._read_float("grid_power") or 0.0
        pv1_w = self._read_float("pv1_power") or 0.0
        pv2_w = self._read_float("pv2_power") or 0.0
        load_w = self._read_float("load_power") or 0.0
        bat_temp = self._read_float("battery_temp")

        # wills106 battery_power_charge: +charge, -discharge
        # PowerSync battery_power_kw:    +discharge, -charge -> negate
        battery_kw = -(bat_w_raw / 1000.0)

        # wills106 measured_power: +import, -export - matches PowerSync
        grid_kw = grid_w / 1000.0

        solar_kw = max(0.0, (pv1_w + pv2_w) / 1000.0)
        load_kw = max(0.0, load_w / 1000.0)

        mode_state = self.hass.states.get(self._entity_map.get("charger_use_mode", ""))
        mode = mode_state.state if mode_state else None

        return {
            "battery_level": soc,
            "battery_power": battery_kw,
            "grid_power": grid_kw,
            "solar_power": solar_kw,
            "load_power": load_kw,
            "battery_temperature": bat_temp,
            "mode": mode,
        }

    # -- Force charge / discharge -----------------------------------------

    async def force_charge(self, duration_minutes: int, power_w: int) -> bool:
        """Force charge from grid for duration_minutes at approximately power_w."""
        from homeassistant.helpers.event import async_call_later

        amps = min(power_w / max(self._nominal_v, 1.0), self._max_charge_a)
        amps = max(0.0, amps)

        _LOGGER.info(
            "Solax force charge: %.1f A (%.0f W / %.1f V) for %d min",
            amps, power_w, self._nominal_v, duration_minutes,
        )

        await self._set_number("charge_current", amps)
        await self._set_select("charger_use_mode", _MODE_MANUAL)
        await self._set_select("manual_mode_select", _MANUAL_CHARGE)
        await self._set_manual_mode_control(_MANUAL_CONTROL_ON)

        self._cancel_timer()
        self._timer_cancel = async_call_later(
            self.hass, duration_minutes * 60, self._timer_restore
        )
        return True

    async def force_discharge(self, duration_minutes: int, power_w: int) -> bool:
        """Force discharge to grid for duration_minutes at approximately power_w."""
        from homeassistant.helpers.event import async_call_later

        amps = min(power_w / max(self._nominal_v, 1.0), self._max_discharge_a)
        amps = max(0.0, amps)

        _LOGGER.info(
            "Solax force discharge: %.1f A (%.0f W / %.1f V) for %d min",
            amps, power_w, self._nominal_v, duration_minutes,
        )

        await self._set_number("discharge_current", amps)
        await self._set_select("charger_use_mode", _MODE_MANUAL)
        await self._set_select("manual_mode_select", _MANUAL_DISCHARGE)
        await self._set_manual_mode_control(_MANUAL_CONTROL_ON)

        self._cancel_timer()
        self._timer_cancel = async_call_later(
            self.hass, duration_minutes * 60, self._timer_restore
        )
        return True

    async def restore_normal(self) -> bool:
        """Restore to Self Use / stop manual mode."""
        self._cancel_timer()
        await self._set_select("manual_mode_select", _MANUAL_STOP)
        await self._set_manual_mode_control(_MANUAL_CONTROL_OFF)
        await self._set_select("charger_use_mode", _MODE_SELF_USE)
        _LOGGER.info("Solax restored to Self Use mode")
        return True

    # -- Reserve / mode / export ------------------------------------------

    async def set_backup_reserve(self, percent: int) -> bool:
        """Set backup reserve (minimum SOC). Clamped to [15, 100]."""
        clamped = max(15, min(100, int(percent)))
        await self._set_number("backup_reserve", clamped)
        _LOGGER.info("Solax backup reserve set to %d%%", clamped)
        return True

    async def set_operation_mode(self, mode: str) -> bool:
        """Map PowerSync operation mode to Solax charger_use_mode."""
        option = _OP_MODE_MAP.get(mode)
        if not option:
            _LOGGER.warning("Solax: unknown operation mode '%s'", mode)
            return False
        await self._set_select("charger_use_mode", option)
        _LOGGER.info("Solax operation mode set to '%s' (%s)", option, mode)
        return True

    async def set_grid_export_limit(self, watts: int) -> bool:
        """Set grid export limit in watts."""
        entity_id = self._entity_map.get("export_limit")
        if not entity_id or self.hass.states.get(entity_id) is None:
            _LOGGER.debug("Solax: export_control_user_limit entity not found, skipping")
            return False
        await self._set_number("export_limit", max(0, watts))
        return True

    async def curtail(self, home_load_w: int | None = None) -> bool:
        """Apply load-following curtailment or zero-export."""
        limit_w = max(0, home_load_w or 0)
        return await self.set_grid_export_limit(limit_w)

    async def restore(self) -> bool:
        """Remove export limit (99999 W effectively disables it)."""
        return await self.set_grid_export_limit(99999)

    async def disconnect(self) -> None:
        """No persistent connection to close."""
        self._cancel_timer()

    # -- Internals ---------------------------------------------------------

    def _discover_entities(self) -> None:
        """Populate the logical entity map from config entry or legacy prefix."""
        self._entity_map = {}

        if self._solax_entry_id:
            registry = er.async_get(self.hass)
            entries = er.async_entries_for_config_entry(registry, self._solax_entry_id)
            entity_ids = [entry.entity_id for entry in entries if entry.entity_id]
            if entity_ids and not self._prefix:
                first_entity = entity_ids[0].split(".", 1)[1]
                self._prefix = first_entity.rsplit("_", 1)[0]
            self._discover_entities_from_ids(entity_ids)
            return

        entity_ids = [
            state.entity_id
            for state in self.hass.states.async_all()
            if state.entity_id.startswith(("sensor.", "number.", "select."))
        ]
        self._discover_entities_from_ids(entity_ids, legacy_prefix=self._prefix)

    def _discover_entities_from_ids(
        self,
        entity_ids: list[str],
        legacy_prefix: str | None = None,
    ) -> None:
        """Resolve logical keys to concrete entity IDs."""
        for key, suffixes in _READ_ENTITIES.items():
            entity_id = self._resolve_entity_id(entity_ids, "sensor", suffixes, legacy_prefix)
            if entity_id:
                self._entity_map[key] = entity_id

        for key, suffixes in _WRITE_ENTITIES.items():
            domain = "number" if key in (
                "charge_current",
                "discharge_current",
                "backup_reserve",
                "export_limit",
            ) else "select"
            entity_id = self._resolve_entity_id(entity_ids, domain, suffixes, legacy_prefix)
            if entity_id:
                self._entity_map[key] = entity_id

    def _resolve_entity_id(
        self,
        entity_ids: list[str],
        domain: str,
        suffixes: tuple[str, ...],
        legacy_prefix: str | None,
    ) -> str | None:
        """Find a matching entity by suffix, optionally constrained to a prefix."""
        if legacy_prefix:
            for suffix in suffixes:
                candidate = f"{domain}.{legacy_prefix}_{suffix}"
                if self.hass.states.get(candidate) is not None:
                    return candidate
        return self._find_entity_by_suffix(entity_ids, domain, suffixes)

    def _expected_entity_hint(self, key: str) -> str | None:
        """Return a likely entity-id hint for error reporting."""
        suffixes = _READ_ENTITIES.get(key) or _WRITE_ENTITIES.get(key)
        if not suffixes:
            return None
        domain = "sensor"
        if key in _WRITE_ENTITIES:
            domain = "number" if key in (
                "charge_current",
                "discharge_current",
                "backup_reserve",
                "export_limit",
            ) else "select"
        if self._prefix:
            return f"{domain}.{self._prefix}_{suffixes[0]}"
        return None

    def _read_float(self, key: str) -> float | None:
        entity_id = self._entity_map.get(key)
        if not entity_id:
            return None
        state = self.hass.states.get(entity_id)
        if not state or state.state in ("unavailable", "unknown", ""):
            return None
        try:
            return float(state.state)
        except (ValueError, TypeError):
            return None

    async def _set_number(self, key: str, value: float) -> None:
        entity_id = self._entity_map.get(key)
        if not entity_id:
            raise ValueError(f"Missing Solax number entity for {key}")
        await self.hass.services.async_call(
            "number",
            "set_value",
            {"entity_id": entity_id, "value": value},
            blocking=True,
        )

    async def _set_select(self, key: str, option: str) -> None:
        entity_id = self._entity_map.get(key)
        if not entity_id:
            raise ValueError(f"Missing Solax select entity for {key}")
        try:
            await self.hass.services.async_call(
                "select",
                "select_option",
                {"entity_id": entity_id, "option": option},
                blocking=True,
            )
        except Exception as exc:
            _LOGGER.warning(
                "Solax: could not set %s to '%s': %s - check wills106 entity labels",
                entity_id,
                option,
                exc,
            )

    async def _set_manual_mode_control(self, option: str) -> None:
        """Toggle manual mode where wills106 exposes a dedicated control select."""
        entity_id = self._entity_map.get("manual_mode_control")
        if not entity_id or self.hass.states.get(entity_id) is None:
            return
        await self._set_select("manual_mode_control", option)

    def _cancel_timer(self) -> None:
        if self._timer_cancel:
            self._timer_cancel()
            self._timer_cancel = None

    async def _timer_restore(self, _now: Any = None) -> None:
        """Auto-restore after force-mode duration expires."""
        _LOGGER.info("Solax force-mode timer expired - restoring Self Use")
        self._timer_cancel = None
        try:
            await self.restore_normal()
        except Exception as exc:
            _LOGGER.error("Solax timer restore failed: %s", exc)
