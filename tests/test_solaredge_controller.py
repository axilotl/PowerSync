"""Tests for SolarEdge active-power curtailment control."""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys
import types


ROOT = Path(__file__).resolve().parent.parent / "custom_components" / "power_sync"

_ps = types.ModuleType("power_sync")
_ps.__path__ = [str(ROOT)]
sys.modules.setdefault("power_sync", _ps)

_inverters = types.ModuleType("power_sync.inverters")
_inverters.__path__ = [str(ROOT / "inverters")]
sys.modules.setdefault("power_sync.inverters", _inverters)

from power_sync.inverters.solaredge import SolarEdgeController


def test_solaredge_load_following_maps_watts_to_percent():
    controller = SolarEdgeController(
        host="",
        rated_power_w=5000,
    )
    writes: list[int] = []

    async def fake_set(percent: int) -> bool:
        writes.append(percent)
        return True

    controller._set_active_power_limit = fake_set

    assert asyncio.run(controller.curtail(home_load_w=1251))
    assert writes == [26]


def test_solaredge_zero_curtail_and_restore_write_percent_limits():
    controller = SolarEdgeController(
        host="",
        rated_power_w=5000,
    )
    writes: list[int] = []

    async def fake_set(percent: int) -> bool:
        writes.append(percent)
        return True

    controller._set_active_power_limit = fake_set

    assert asyncio.run(controller.curtail())
    assert asyncio.run(controller.restore())
    assert writes == [0, 100]


def test_solaredge_entity_fallback_prefers_configured_prefix():
    class State:
        def __init__(self, state: str) -> None:
            self.state = state

    class States:
        def __init__(self) -> None:
            self._states = {
                "number.custom_active_power_limit": State("100"),
                "number.solaredge_active_power_limit": State("100"),
            }

        def get(self, entity_id: str):
            return self._states.get(entity_id)

    class Services:
        def __init__(self) -> None:
            self.calls: list[tuple[str, str, dict]] = []

        async def async_call(self, domain: str, service: str, data: dict, blocking: bool = False):
            self.calls.append((domain, service, data))

    class Hass:
        def __init__(self) -> None:
            self.states = States()
            self.services = Services()

    hass = Hass()
    controller = SolarEdgeController(
        host="",
        entity_prefix="custom",
        hass=hass,
    )

    assert asyncio.run(controller.connect())
    assert asyncio.run(controller.curtail(home_load_w=1000))
    assert hass.services.calls == [
        (
            "number",
            "set_value",
            {"entity_id": "number.custom_active_power_limit", "value": 20},
        )
    ]
