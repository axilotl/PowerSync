"""Regression tests for SAJ H2 force-mode controls."""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys
import types


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"


def _install_stubs() -> None:
    ha_root = types.ModuleType("homeassistant")
    ha_helpers = types.ModuleType("homeassistant.helpers")
    ha_entity_registry = types.ModuleType("homeassistant.helpers.entity_registry")

    ha_entity_registry.async_get = lambda hass: hass.entity_registry
    ha_entity_registry.async_entries_for_config_entry = lambda registry, entry_id: []

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

from power_sync.inverters.saj_h2 import SajH2BatteryController  # noqa: E402


class _FakeState:
    def __init__(self, entity_id: str, state: str = "0"):
        self.entity_id = entity_id
        self.state = state
        self.attributes = {}


class _FakeStates:
    def __init__(self, states: list[_FakeState]):
        self._states = {state.entity_id: state for state in states}

    def get(self, entity_id: str | None):
        return self._states.get(entity_id or "")

    def set(self, entity_id: str, state: str) -> None:
        self._states[entity_id] = _FakeState(entity_id, state)


class _FakeServices:
    def __init__(
        self,
        states: _FakeStates,
        *,
        switch_turn_on_sticks: bool = True,
        fail_on: tuple[str, str, str] | None = None,
        mirror_app_mode: bool = True,
    ):
        self._states = states
        self._switch_turn_on_sticks = switch_turn_on_sticks
        self._fail_on = fail_on
        self._mirror_app_mode = mirror_app_mode
        self.calls: list[tuple[str, str, dict]] = []

    async def async_call(self, domain: str, service: str, data: dict, blocking: bool = True):
        self.calls.append((domain, service, dict(data)))
        entity_id = data.get("entity_id")
        if self._fail_on == (domain, service, entity_id):
            raise RuntimeError("service failed")
        if domain == "number" and service == "set_value":
            self._states.set(entity_id, str(data["value"]))
            if self._mirror_app_mode and entity_id == "number.saj_app_mode_input":
                self._states.set("sensor.saj_app_mode", str(data["value"]))
        elif domain == "text" and service == "set_value":
            self._states.set(entity_id, str(data["value"]))
        elif domain == "switch" and service == "turn_on" and self._switch_turn_on_sticks:
            self._states.set(entity_id, "on")
        elif domain == "switch" and service == "turn_off":
            self._states.set(entity_id, "off")


class _FakeHass:
    def __init__(
        self,
        states: list[_FakeState],
        *,
        switch_turn_on_sticks: bool = True,
        fail_on: tuple[str, str, str] | None = None,
        mirror_app_mode: bool = True,
    ):
        self.states = _FakeStates(states)
        self.services = _FakeServices(
            self.states,
            switch_turn_on_sticks=switch_turn_on_sticks,
            fail_on=fail_on,
            mirror_app_mode=mirror_app_mode,
        )
        self.entity_registry = object()


def _passive_states(
    *,
    charge_power: str = "0",
    discharge_power: str = "0",
    passive_charge_control: str = "off",
) -> list[_FakeState]:
    return [
        _FakeState("number.saj_passive_bat_charge_power_input", charge_power),
        _FakeState("number.saj_passive_bat_discharge_power_input", discharge_power),
        _FakeState("switch.saj_passive_charge_control", passive_charge_control),
        _FakeState("sensor.saj_inverter_working_mode", "2"),
        _FakeState("sensor.saj_r_phase_inverter_voltage", "0"),
    ]


def _tou_states(
    *,
    charge_bitmask: str = "0",
    discharge_bitmask: str = "0",
    passive_charge_control: str = "off",
    passive_discharge_control: str = "off",
    charging_control: str = "off",
    discharging_control: str = "off",
) -> list[_FakeState]:
    return [
        _FakeState("text.saj_charge7_start_time_time", "00:00"),
        _FakeState("text.saj_charge7_end_time_time", "23:59"),
        _FakeState("number.saj_charge7_day_mask_input", "0"),
        _FakeState("number.saj_charge7_power_percent_input", "0"),
        _FakeState("text.saj_discharge7_start_time_time", "00:00"),
        _FakeState("text.saj_discharge7_end_time_time", "23:59"),
        _FakeState("number.saj_discharge7_day_mask_input", "0"),
        _FakeState("number.saj_discharge7_power_percent_input", "0"),
        _FakeState("number.saj_charge_time_enable_input", charge_bitmask),
        _FakeState("number.saj_discharge_time_enable_input", discharge_bitmask),
        _FakeState("sensor.saj_charge_time_enable_bitmask", charge_bitmask),
        _FakeState("sensor.saj_discharge_time_enable_bitmask", discharge_bitmask),
        _FakeState("sensor.saj_app_mode", "0"),
        _FakeState("number.saj_app_mode_input", "0"),
        _FakeState("sensor.saj_inverter_working_mode", "2"),
        _FakeState("sensor.saj_r_phase_inverter_voltage", "0"),
        _FakeState("switch.saj_passive_charge_control", passive_charge_control),
        _FakeState("switch.saj_passive_discharge_control", passive_discharge_control),
        _FakeState("switch.saj_charging_control", charging_control),
        _FakeState("switch.saj_discharging_control", discharging_control),
    ]


def _controller(hass: _FakeHass) -> SajH2BatteryController:
    controller = SajH2BatteryController(hass, saj_entry_id="saj-entry")
    controller._SWITCH_VERIFY_DELAY_SEC = 0
    controller._entity_map = {
        "charge_power": "number.saj_passive_bat_charge_power_input",
        "discharge_power": "number.saj_passive_bat_discharge_power_input",
        "passive_charge_control": "switch.saj_passive_charge_control",
        "inverter_working_mode": "sensor.saj_inverter_working_mode",
        "inverter_voltage_r": "sensor.saj_r_phase_inverter_voltage",
    }
    return controller


def _tou_controller(hass: _FakeHass) -> SajH2BatteryController:
    controller = SajH2BatteryController(hass, saj_entry_id="saj-entry")
    controller._entity_map = {
        "charge7_start_time": "text.saj_charge7_start_time_time",
        "charge7_end_time": "text.saj_charge7_end_time_time",
        "charge7_day_mask": "number.saj_charge7_day_mask_input",
        "charge7_power_percent": "number.saj_charge7_power_percent_input",
        "discharge7_start_time": "text.saj_discharge7_start_time_time",
        "discharge7_end_time": "text.saj_discharge7_end_time_time",
        "discharge7_day_mask": "number.saj_discharge7_day_mask_input",
        "discharge7_power_percent": "number.saj_discharge7_power_percent_input",
        "charge_time_enable": "number.saj_charge_time_enable_input",
        "discharge_time_enable": "number.saj_discharge_time_enable_input",
        "charge_time_enable_bitmask": "sensor.saj_charge_time_enable_bitmask",
        "discharge_time_enable_bitmask": "sensor.saj_discharge_time_enable_bitmask",
        "app_mode": "sensor.saj_app_mode",
        "app_mode_writable": "number.saj_app_mode_input",
        "inverter_working_mode": "sensor.saj_inverter_working_mode",
        "inverter_voltage_r": "sensor.saj_r_phase_inverter_voltage",
    }
    return controller


def _tou_controller_with_switches(hass: _FakeHass) -> SajH2BatteryController:
    controller = _tou_controller(hass)
    controller._entity_map.update(
        {
            "passive_charge_control": "switch.saj_passive_charge_control",
            "passive_discharge_control": "switch.saj_passive_discharge_control",
            "charging_control": "switch.saj_charging_control",
            "discharging_control": "switch.saj_discharging_control",
        }
    )
    return controller


def test_force_charge_fails_when_charge_slot_entities_are_unmapped():
    hass = _FakeHass(_tou_states())
    controller = _controller(hass)

    assert not asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))
    assert hass.services.calls == []


def test_force_charge_uses_tou_charge_slot_7_and_clears_discharge_slots():
    hass = _FakeHass(_tou_states(charge_bitmask="2", discharge_bitmask="5"))
    controller = _tou_controller(hass)

    assert asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))

    assert hass.services.calls == [
        (
            "text",
            "set_value",
            {"entity_id": "text.saj_charge7_start_time_time", "value": "00:00"},
        ),
        (
            "text",
            "set_value",
            {"entity_id": "text.saj_charge7_end_time_time", "value": "23:59"},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.saj_charge7_day_mask_input", "value": 127},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.saj_charge7_power_percent_input", "value": 100},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.saj_discharge_time_enable_input", "value": 0},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.saj_charge_time_enable_input", "value": 66},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.saj_app_mode_input", "value": 1},
        ),
    ]
    assert controller._cached_discharge_enable == 5
    assert hass.states.get("sensor.saj_app_mode").state == "1"


def test_force_charge_clears_stale_switch_controls_before_tou_slot_control():
    hass = _FakeHass(
        _tou_states(
            passive_charge_control="on",
            passive_discharge_control="on",
            charging_control="on",
            discharging_control="on",
        )
    )
    controller = _tou_controller_with_switches(hass)

    assert asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))

    assert hass.services.calls[:4] == [
        (
            "switch",
            "turn_off",
            {"entity_id": "switch.saj_passive_charge_control"},
        ),
        (
            "switch",
            "turn_off",
            {"entity_id": "switch.saj_passive_discharge_control"},
        ),
        (
            "switch",
            "turn_off",
            {"entity_id": "switch.saj_charging_control"},
        ),
        (
            "switch",
            "turn_off",
            {"entity_id": "switch.saj_discharging_control"},
        ),
    ]
    assert hass.states.get("switch.saj_passive_charge_control").state == "off"
    assert hass.states.get("sensor.saj_app_mode").state == "1"


def test_force_discharge_clears_stale_switch_controls_before_tou_slot_control():
    hass = _FakeHass(
        _tou_states(
            passive_charge_control="on",
            passive_discharge_control="on",
            charging_control="on",
            discharging_control="on",
        )
    )
    controller = _tou_controller_with_switches(hass)

    assert asyncio.run(controller.force_discharge(duration_minutes=30, power_w=2500))

    assert hass.services.calls[:4] == [
        (
            "switch",
            "turn_off",
            {"entity_id": "switch.saj_passive_charge_control"},
        ),
        (
            "switch",
            "turn_off",
            {"entity_id": "switch.saj_passive_discharge_control"},
        ),
        (
            "switch",
            "turn_off",
            {"entity_id": "switch.saj_charging_control"},
        ),
        (
            "switch",
            "turn_off",
            {"entity_id": "switch.saj_discharging_control"},
        ),
    ]
    assert hass.states.get("switch.saj_passive_charge_control").state == "off"
    assert hass.states.get("sensor.saj_app_mode").state == "1"


def test_restore_normal_after_force_charge_clears_charge_slot_and_restores_discharge_slots():
    hass = _FakeHass(_tou_states(charge_bitmask="64", discharge_bitmask="3"))
    controller = _tou_controller(hass)

    assert asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))
    assert asyncio.run(controller.restore_normal())

    assert (
        "number",
        "set_value",
        {"entity_id": "number.saj_charge_time_enable_input", "value": 0},
    ) in hass.services.calls
    assert (
        "number",
        "set_value",
        {"entity_id": "number.saj_discharge_time_enable_input", "value": 3},
    ) in hass.services.calls
    assert (
        "number",
        "set_value",
        {"entity_id": "number.saj_app_mode_input", "value": 0},
    ) in hass.services.calls
    assert controller._cached_discharge_enable is None


def test_force_charge_attempts_restore_normal_on_mid_sequence_exception():
    hass = _FakeHass(
        _tou_states(),
        fail_on=(
            "number",
            "set_value",
            "number.saj_charge7_power_percent_input",
        ),
    )
    controller = _tou_controller(hass)
    restore_calls = 0

    async def restore_normal():
        nonlocal restore_calls
        restore_calls += 1
        return True

    controller.restore_normal = restore_normal

    assert not asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))
    assert restore_calls == 1


def test_set_idle_fails_when_passive_switch_does_not_stick_on():
    hass = _FakeHass(_passive_states(), switch_turn_on_sticks=False)
    controller = _controller(hass)

    assert not asyncio.run(controller.set_idle())

    assert (
        "switch",
        "turn_on",
        {"entity_id": "switch.saj_passive_charge_control"},
    ) in hass.services.calls
    assert hass.states.get("switch.saj_passive_charge_control").state == "off"


def test_set_idle_drives_and_verifies_passive_app_mode_when_mapped():
    hass = _FakeHass(
        _passive_states()
        + [
            _FakeState("sensor.saj_app_mode", "0"),
            _FakeState("number.saj_app_mode_input", "0"),
        ],
    )
    controller = _controller(hass)
    controller._APP_MODE_VERIFY_DELAY_SEC = 0
    controller._entity_map["app_mode"] = "sensor.saj_app_mode"
    controller._entity_map["app_mode_writable"] = "number.saj_app_mode_input"

    assert asyncio.run(controller.set_idle())

    assert (
        "number",
        "set_value",
        {"entity_id": "number.saj_app_mode_input", "value": 3},
    ) in hass.services.calls
    assert hass.states.get("sensor.saj_app_mode").state == "3"
