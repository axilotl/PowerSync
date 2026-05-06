"""Regression tests for SAJ H2 passive force-charge controls."""

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
    ):
        self._states = states
        self._switch_turn_on_sticks = switch_turn_on_sticks
        self._fail_on = fail_on
        self.calls: list[tuple[str, str, dict]] = []

    async def async_call(self, domain: str, service: str, data: dict, blocking: bool = True):
        self.calls.append((domain, service, dict(data)))
        entity_id = data.get("entity_id")
        if self._fail_on == (domain, service, entity_id):
            raise RuntimeError("service failed")
        if domain == "number" and service == "set_value":
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
    ):
        self.states = _FakeStates(states)
        self.services = _FakeServices(
            self.states,
            switch_turn_on_sticks=switch_turn_on_sticks,
            fail_on=fail_on,
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


def test_force_charge_fails_when_passive_entities_are_unavailable():
    hass = _FakeHass(_passive_states(charge_power="unavailable"))
    controller = _controller(hass)

    assert not asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))
    assert hass.services.calls == []


def test_force_charge_fails_when_passive_switch_does_not_stick_on():
    hass = _FakeHass(_passive_states(), switch_turn_on_sticks=False)
    controller = _controller(hass)

    assert not asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))

    assert (
        "switch",
        "turn_on",
        {"entity_id": "switch.saj_passive_charge_control"},
    ) in hass.services.calls
    assert hass.states.get("switch.saj_passive_charge_control").state == "off"


def test_force_charge_succeeds_when_passive_switch_becomes_on():
    hass = _FakeHass(_passive_states())
    controller = _controller(hass)

    assert asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))

    assert hass.services.calls[:3] == [
        (
            "number",
            "set_value",
            {"entity_id": "number.saj_passive_bat_discharge_power_input", "value": 0},
        ),
        (
            "number",
            "set_value",
            {"entity_id": "number.saj_passive_bat_charge_power_input", "value": 250},
        ),
        (
            "switch",
            "turn_on",
            {"entity_id": "switch.saj_passive_charge_control"},
        ),
    ]
    assert hass.states.get("switch.saj_passive_charge_control").state == "on"


def test_force_charge_attempts_restore_normal_on_mid_sequence_exception():
    hass = _FakeHass(
        _passive_states(),
        fail_on=(
            "number",
            "set_value",
            "number.saj_passive_bat_charge_power_input",
        ),
    )
    controller = _controller(hass)
    restore_calls = 0

    async def restore_normal():
        nonlocal restore_calls
        restore_calls += 1
        return True

    controller.restore_normal = restore_normal

    assert not asyncio.run(controller.force_charge(duration_minutes=30, power_w=2500))
    assert restore_calls == 1
