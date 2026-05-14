"""Tests for Sigenergy EVAC/EVDC Modbus charger control."""

from __future__ import annotations

import asyncio
import importlib
import sys
import types
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"
_SENTINEL = object()
_STUB_MODULE_NAMES = (
    "power_sync",
    "pymodbus",
    "pymodbus.client",
    "pymodbus.exceptions",
)


@pytest.fixture()
def charger_module():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    saved_modules = {name: sys.modules.get(name, _SENTINEL) for name in _STUB_MODULE_NAMES}
    for name in _STUB_MODULE_NAMES:
        sys.modules.pop(name, None)

    power_sync = types.ModuleType("power_sync")
    power_sync.__path__ = [str(COMPONENT_ROOT)]
    sys.modules["power_sync"] = power_sync

    pymodbus = types.ModuleType("pymodbus")
    pymodbus.__version__ = "3.8.0"
    pymodbus_client = types.ModuleType("pymodbus.client")
    pymodbus_exceptions = types.ModuleType("pymodbus.exceptions")

    class _AsyncModbusTcpClient:
        connected = False

        def __init__(self, *args, **kwargs) -> None:
            pass

    pymodbus_client.AsyncModbusTcpClient = _AsyncModbusTcpClient
    pymodbus_exceptions.ModbusException = type("ModbusException", (Exception,), {})
    sys.modules["pymodbus"] = pymodbus
    sys.modules["pymodbus.client"] = pymodbus_client
    sys.modules["pymodbus.exceptions"] = pymodbus_exceptions

    try:
        yield importlib.import_module("power_sync.sigenergy_charger")
    finally:
        sys.modules.pop("power_sync.sigenergy_charger", None)
        for name in _STUB_MODULE_NAMES:
            if saved_modules[name] is _SENTINEL:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = saved_modules[name]
        loop.close()
        asyncio.set_event_loop(None)


def test_evac_start_sets_output_current_before_start(charger_module):
    controller = charger_module.SigenergyEVChargerController(
        host="192.0.2.10",
        slave_id=1,
        charger_type="evac",
    )
    writes: list[tuple[int, list[int]]] = []

    async def read(address, count):
        assert address == controller.REG_EVAC_RATED_CURRENT
        assert count == 5
        return [0, 3200, 0, 0, 4000]

    async def write(address, values):
        writes.append((address, list(values)))
        return True

    controller._read_input_registers = read
    controller._write_holding_registers = write

    assert asyncio.run(controller.start_charging(16))

    assert writes == [
        (controller.REG_EVAC_OUTPUT_CURRENT, [0, 1600]),
        (controller.REG_EVAC_START_STOP, [controller.EVAC_COMMAND_START]),
    ]


def test_evac_state_decodes_status_power_energy_and_current_limit(charger_module):
    controller = charger_module.SigenergyEVChargerController(
        host="192.0.2.10",
        charger_type="evac",
    )

    async def read(address, count):
        assert address == controller.REG_EVAC_SYSTEM_STATE
        assert count == 12
        return [
            0x05,  # C2
            0,
            12345,  # 123.45 kWh
            0,
            7200,  # 7.2 kW
            0,
            0,
            0,
            2200,  # 22A rated
            2300,  # 230V
            0,
            2000,  # 20A breaker
        ]

    controller._read_input_registers = read

    state = asyncio.run(controller.read_state())

    assert state.status == "c2"
    assert state.is_connected is True
    assert state.is_charging is True
    assert state.power_kw == 7.2
    assert state.energy_kwh == 123.45
    assert state.rated_current_a == 20


def test_evdc_uses_inverter_start_stop_register_and_rejects_current_limit(charger_module):
    controller = charger_module.SigenergyEVChargerController(
        host="192.0.2.10",
        slave_id=2,
        charger_type="evdc",
    )
    writes: list[tuple[int, list[int]]] = []

    async def write(address, values):
        writes.append((address, list(values)))
        return True

    controller._write_holding_registers = write

    assert asyncio.run(controller.start_charging(32))
    assert not asyncio.run(controller.set_charging_amps(32))
    assert asyncio.run(controller.stop_charging())

    assert writes == [
        (controller.REG_EVDC_START_STOP, [controller.EVDC_COMMAND_START]),
        (controller.REG_EVDC_START_STOP, [controller.EVDC_COMMAND_STOP]),
    ]
