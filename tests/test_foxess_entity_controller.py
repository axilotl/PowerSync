"""Regression tests for the FoxESS foxess_modbus entity bridge."""

from __future__ import annotations

import asyncio
from pathlib import Path
from types import SimpleNamespace
import sys
import types

import pytest


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"


def _install_stubs() -> None:
    ha_root = types.ModuleType("homeassistant")
    ha_helpers = types.ModuleType("homeassistant.helpers")
    ha_entity_registry = types.ModuleType("homeassistant.helpers.entity_registry")

    ha_entity_registry.async_get = lambda hass: hass.entity_registry
    ha_entity_registry.async_entries_for_config_entry = (
        lambda registry, entry_id: registry.entries_for(entry_id)
    )

    ha_helpers.entity_registry = ha_entity_registry
    ha_root.helpers = ha_helpers

    sys.modules["homeassistant"] = ha_root
    sys.modules["homeassistant.helpers"] = ha_helpers
    sys.modules["homeassistant.helpers.entity_registry"] = ha_entity_registry

    power_sync = types.ModuleType("power_sync")
    power_sync.__path__ = [str(COMPONENT_ROOT)]
    sys.modules["power_sync"] = power_sync

    inverters = types.ModuleType("power_sync.inverters")
    inverters.__path__ = [str(COMPONENT_ROOT / "inverters")]
    sys.modules["power_sync.inverters"] = inverters


_install_stubs()

from power_sync.inverters.foxess_entity import FoxESSEntityController  # noqa: E402


class _FakeState:
    def __init__(
        self,
        entity_id: str,
        state: str = "0",
        attributes: dict | None = None,
    ) -> None:
        self.entity_id = entity_id
        self.state = state
        self.attributes = attributes or {}


class _FakeStates:
    def __init__(self, states: list[_FakeState]) -> None:
        self._states = {state.entity_id: state for state in states}

    def get(self, entity_id: str | None):
        return self._states.get(entity_id or "")

    def async_all(self, domain: str | None = None):
        if domain is None:
            return list(self._states.values())
        prefix = f"{domain}."
        return [
            state
            for state in self._states.values()
            if state.entity_id.startswith(prefix)
        ]


class _FakeServices:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict]] = []

    async def async_call(
        self,
        domain: str,
        service: str,
        data: dict,
        blocking: bool = True,
    ) -> None:
        self.calls.append((domain, service, dict(data)))


class _FakeRegistry:
    def __init__(self, entries: dict[str, list[str]] | None = None) -> None:
        self._entries = entries or {}

    def entries_for(self, entry_id: str):
        return [
            SimpleNamespace(entity_id=entity_id)
            for entity_id in self._entries.get(entry_id, [])
        ]


class _FakeHass:
    def __init__(
        self,
        states: list[_FakeState],
        registry_entries: dict[str, list[str]] | None = None,
    ) -> None:
        self.states = _FakeStates(states)
        self.services = _FakeServices()
        self.entity_registry = _FakeRegistry(registry_entries)


def _kw() -> dict[str, str]:
    return {"unit_of_measurement": "kW"}


def _kwh() -> dict[str, str]:
    return {"unit_of_measurement": "kWh"}


def _base_states(prefix: str = "foxess") -> list[_FakeState]:
    return [
        _FakeState(f"sensor.{prefix}_battery_soc", "62"),
        _FakeState(f"sensor.{prefix}_battery_soh", "97"),
        _FakeState(f"sensor.{prefix}_battery_voltage", "410"),
        _FakeState(f"sensor.{prefix}_battery_temp", "24"),
        _FakeState(f"sensor.{prefix}_invbatpower", "1.4", _kw()),
        _FakeState(f"sensor.{prefix}_grid_ct", "0.6", _kw()),
        _FakeState(f"sensor.{prefix}_pv_power_now", "4.2", _kw()),
        _FakeState(f"sensor.{prefix}_load_power", "2.2", _kw()),
        _FakeState(f"sensor.{prefix}_pv1_power", "2.1", _kw()),
        _FakeState(f"sensor.{prefix}_pv1_voltage", "405"),
        _FakeState(f"sensor.{prefix}_pv1_current", "5.2"),
        _FakeState(f"sensor.{prefix}_solar_energy_today", "12.5", _kwh()),
        _FakeState(f"sensor.{prefix}_grid_consumption_energy_today", "3.1", _kwh()),
        _FakeState(f"sensor.{prefix}_feed_in_energy_today", "4.4", _kwh()),
        _FakeState(f"sensor.{prefix}_battery_charge_today", "5.6", _kwh()),
        _FakeState(f"sensor.{prefix}_battery_discharge_today", "4.8", _kwh()),
        _FakeState(
            f"select.{prefix}_work_mode",
            "Self Use",
            {
                "options": [
                    "Self Use",
                    "Feed-in First",
                    "Back-up",
                    "Force Charge",
                    "Force Discharge",
                ],
            },
        ),
        _FakeState(f"number.{prefix}_force_charge_power", "0", _kw()),
        _FakeState(f"number.{prefix}_force_discharge_power", "0", _kw()),
        _FakeState(f"number.{prefix}_min_soc_on_grid", "20"),
        _FakeState(f"number.{prefix}_max_charge_current", "25"),
        _FakeState(f"number.{prefix}_max_discharge_current", "25"),
        _FakeState(f"number.{prefix}_export_power_limit", "99999"),
    ]


def _without_suffix(states: list[_FakeState], suffixes: tuple[str, ...]) -> list[_FakeState]:
    return [
        state
        for state in states
        if not any(state.entity_id.endswith(suffix) for suffix in suffixes)
    ]


def test_prefix_discovery_maps_telemetry_and_daily_energy():
    hass = _FakeHass(_base_states())
    controller = FoxESSEntityController(hass, entity_prefix="foxess")

    assert asyncio.run(controller.connect())
    status = controller.get_status()

    assert status["battery_level"] == 62.0
    assert status["battery_soh"] == 97.0
    assert status["battery_temperature"] == 24.0
    assert status["battery_power"] == 1.4
    assert status["grid_power"] == -0.6
    assert status["solar_power"] == 4.2
    assert status["load_power"] == 2.2
    assert status["backup_reserve"] == 20.0
    assert status["daily_solar_energy_kwh"] == 12.5
    assert status["daily_grid_import_kwh"] == 3.1
    assert status["daily_grid_export_kwh"] == 4.4
    assert status["daily_battery_charge_kwh"] == 5.6
    assert status["daily_battery_discharge_kwh"] == 4.8
    assert status["pv1_power"] == 2.1
    assert status["pv1_voltage"] == 405.0
    assert status["pv1_current"] == 5.2
    assert status["battery_max_charge_power_w"] == 10250


def test_fallback_sensors_normalize_grid_and_battery_signs():
    states = _without_suffix(_base_states(), ("_invbatpower", "_grid_ct"))
    states.extend(
        [
            _FakeState("sensor.foxess_battery_charge", "0.2", _kw()),
            _FakeState("sensor.foxess_battery_discharge", "0.7", _kw()),
            _FakeState("sensor.foxess_grid_consumption", "1.2", _kw()),
            _FakeState("sensor.foxess_feed_in", "0.3", _kw()),
        ]
    )
    hass = _FakeHass(states)
    controller = FoxESSEntityController(hass, entity_prefix="foxess")

    assert asyncio.run(controller.connect())
    status = controller.get_status()

    assert status["battery_power"] == pytest.approx(0.5)
    assert status["grid_power"] == pytest.approx(0.9)


def test_selected_config_entry_is_preferred_before_suffix_fallback():
    preferred_states = _base_states(prefix="renamed_fox")
    fallback_states = _base_states(prefix="foxess")
    registry_ids = [state.entity_id for state in preferred_states]
    hass = _FakeHass(
        preferred_states + fallback_states,
        registry_entries={"fox-entry": registry_ids},
    )
    controller = FoxESSEntityController(hass, foxess_entry_id="fox-entry")

    assert asyncio.run(controller.connect())

    assert controller._entity_map["battery_level"] == "sensor.renamed_fox_battery_soc"
    assert controller._entity_map["work_mode"] == "select.renamed_fox_work_mode"
    assert controller._entity_map["force_charge_power"] == (
        "number.renamed_fox_force_charge_power"
    )


def test_selected_config_entry_falls_back_to_live_suffix_discovery():
    states = _base_states()
    hass = _FakeHass(
        states,
        registry_entries={
            "fox-entry": [
                "sensor.foxess_battery_soc",
                "sensor.foxess_grid_ct",
            ],
        },
    )
    controller = FoxESSEntityController(hass, foxess_entry_id="fox-entry")

    assert asyncio.run(controller.connect())

    assert controller._entity_map["battery_level"] == "sensor.foxess_battery_soc"
    assert controller._entity_map["work_mode"] == "select.foxess_work_mode"
    assert controller._entity_map["force_discharge_power"] == (
        "number.foxess_force_discharge_power"
    )


def test_force_restore_reserve_work_mode_and_limit_controls():
    hass = _FakeHass(_base_states())
    controller = FoxESSEntityController(hass, entity_prefix="foxess")

    assert asyncio.run(controller.connect())
    assert asyncio.run(controller.force_charge(duration_minutes=30, power_w=5000))
    assert asyncio.run(controller.force_discharge(duration_minutes=30, power_w=4200))
    assert asyncio.run(controller.restore_normal())
    assert asyncio.run(controller.set_backup_reserve(33))
    assert asyncio.run(controller.set_work_mode("feed_in"))
    assert asyncio.run(controller.set_work_mode("backup"))
    assert asyncio.run(controller.set_charge_rate_limit(18))
    assert asyncio.run(controller.set_discharge_rate_limit(22))
    assert asyncio.run(controller.curtail(1500))

    assert hass.services.calls == [
        (
            "number",
            "set_value",
            {"entity_id": "number.foxess_force_charge_power", "value": 5.0},
        ),
        (
            "select",
            "select_option",
            {"entity_id": "select.foxess_work_mode", "option": "Force Charge"},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.foxess_force_discharge_power", "value": 4.2},
        ),
        (
            "select",
            "select_option",
            {"entity_id": "select.foxess_work_mode", "option": "Force Discharge"},
        ),
        (
            "select",
            "select_option",
            {"entity_id": "select.foxess_work_mode", "option": "Self Use"},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.foxess_min_soc_on_grid", "value": 33},
        ),
        (
            "select",
            "select_option",
            {"entity_id": "select.foxess_work_mode", "option": "Feed-in First"},
        ),
        (
            "select",
            "select_option",
            {"entity_id": "select.foxess_work_mode", "option": "Back-up"},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.foxess_max_charge_current", "value": 18.0},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.foxess_max_discharge_current", "value": 22.0},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.foxess_export_power_limit", "value": 1500},
        ),
    ]


def test_curtailment_returns_false_when_export_limit_is_missing():
    states = _without_suffix(_base_states(), ("_export_power_limit",))
    hass = _FakeHass(states)
    controller = FoxESSEntityController(hass, entity_prefix="foxess")

    assert asyncio.run(controller.connect())
    assert not asyncio.run(controller.curtail(1500))
    assert hass.services.calls == []


def test_missing_required_entities_raise_actionable_setup_error():
    states = _without_suffix(_base_states(), ("_force_charge_power",))
    hass = _FakeHass(states)
    controller = FoxESSEntityController(hass, entity_prefix="foxess")

    with pytest.raises(ValueError) as exc:
        asyncio.run(controller.connect())

    message = str(exc.value)
    assert message.startswith("foxess_missing_entities:")
    assert "number.foxess_force_charge_power" in message


def test_read_only_reserve_sensor_does_not_satisfy_writable_requirement():
    states = _without_suffix(_base_states(), ("_min_soc_on_grid",))
    states.append(_FakeState("sensor.foxess_min_soc", "20"))
    hass = _FakeHass(states)
    controller = FoxESSEntityController(hass, entity_prefix="foxess")

    with pytest.raises(ValueError) as exc:
        asyncio.run(controller.connect())

    assert "number.foxess_min_soc_on_grid" in str(exc.value)
