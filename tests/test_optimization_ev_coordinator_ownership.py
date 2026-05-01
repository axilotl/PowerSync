"""Tests for the legacy optimizer EV coordinator ownership guard."""

from __future__ import annotations

import asyncio
import importlib
import sys
import types
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "custom_components" / "power_sync"


def _install_ha_stubs() -> None:
    ha_root = sys.modules.setdefault("homeassistant", types.ModuleType("homeassistant"))
    ha_core = sys.modules.setdefault("homeassistant.core", types.ModuleType("homeassistant.core"))
    ha_util = sys.modules.setdefault("homeassistant.util", types.ModuleType("homeassistant.util"))
    ha_dt = sys.modules.setdefault("homeassistant.util.dt", types.ModuleType("homeassistant.util.dt"))

    ha_core.HomeAssistant = type("HomeAssistant", (), {})
    ha_dt.now = lambda *args, **kwargs: datetime.now(timezone.utc)
    ha_util.dt = ha_dt
    ha_root.util = ha_util


_install_ha_stubs()

_ps = types.ModuleType("power_sync")
_ps.__path__ = [str(ROOT)]
sys.modules["power_sync"] = _ps

_automations = types.ModuleType("power_sync.automations")
_automations.__path__ = [str(ROOT / "automations")]
sys.modules["power_sync.automations"] = _automations

_optimization = types.ModuleType("power_sync.optimization")
_optimization.__path__ = [str(ROOT / "optimization")]
sys.modules["power_sync.optimization"] = _optimization

ev_ownership = importlib.import_module("power_sync.automations.ev_ownership")
ev_coordinator = importlib.import_module("power_sync.optimization.ev_coordinator")


class _Entry:
    entry_id = "entry-1"
    data = {}
    options = {}


class _States:
    def get(self, entity_id: str):
        return None


class _Services:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str, dict]] = []

    async def async_call(self, domain: str, service: str, data: dict):
        self.calls.append((domain, service, data))


class _ConfigEntries:
    def async_entries(self, domain: str):
        return []


class _Hass:
    def __init__(self) -> None:
        self.data = {"power_sync": {"entry-1": {}}}
        self.states = _States()
        self.services = _Services()
        self.config_entries = _ConfigEntries()


def test_optimizer_ev_start_is_blocked_by_existing_owner():
    hass = _Hass()
    entry = _Entry()
    config = ev_coordinator.EVConfig(entity_id="switch.garage_ev", name="Garage EV")
    coordinator = ev_coordinator.EVCoordinator(hass, [config], config_entry=entry)

    ev_ownership.claim_ev_ownership(
        hass,
        entry,
        ev_ownership.DEFAULT_VEHICLE_ID,
        owner_mode="solar_surplus",
    )

    result = asyncio.run(coordinator._start_charging(config))

    assert result is False
    assert hass.services.calls == []
    last_command = ev_ownership.get_ev_last_commands(hass, entry)["switch.garage_ev"]
    assert last_command["command"] == "start_ev_coordinator"
    assert last_command["success"] is False
    assert "solar_surplus" in last_command["reason"]


def test_optimizer_ev_start_claims_ownership_after_physical_start():
    hass = _Hass()
    entry = _Entry()
    config = ev_coordinator.EVConfig(entity_id="switch.garage_ev", name="Garage EV")
    coordinator = ev_coordinator.EVCoordinator(hass, [config], config_entry=entry)

    result = asyncio.run(coordinator._start_charging(config))

    assert result is True
    assert hass.services.calls == [
        ("switch", "turn_on", {"entity_id": "switch.garage_ev"})
    ]
    lease = ev_ownership.get_ev_ownerships(hass, entry)["switch.garage_ev"]
    assert lease["owner_mode"] == "ev_coordinator"
    assert lease["last_command"]["command"] == "start_ev_coordinator"


def test_optimizer_ev_stop_refuses_unowned_charging():
    hass = _Hass()
    entry = _Entry()
    config = ev_coordinator.EVConfig(entity_id="switch.garage_ev", name="Garage EV")
    coordinator = ev_coordinator.EVCoordinator(hass, [config], config_entry=entry)

    result = asyncio.run(coordinator._stop_charging(config))

    assert result is False
    assert hass.services.calls == []
    last_command = ev_ownership.get_ev_last_commands(hass, entry)["switch.garage_ev"]
    assert last_command["command"] == "stop_ev_coordinator"
    assert last_command["success"] is False


def test_optimizer_ev_stop_releases_owned_loadpoint():
    hass = _Hass()
    entry = _Entry()
    config = ev_coordinator.EVConfig(entity_id="switch.garage_ev", name="Garage EV")
    coordinator = ev_coordinator.EVCoordinator(hass, [config], config_entry=entry)
    ev_ownership.claim_ev_ownership(
        hass,
        entry,
        "switch.garage_ev",
        owner_mode="ev_coordinator",
    )

    result = asyncio.run(coordinator._stop_charging(config, reason="target reached"))

    assert result is True
    assert hass.services.calls == [
        ("switch", "turn_off", {"entity_id": "switch.garage_ev"})
    ]
    assert ev_ownership.get_ev_ownerships(hass, entry) == {}
    last_command = ev_ownership.get_ev_last_commands(hass, entry)["switch.garage_ev"]
    assert last_command["command"] == "stop_ev_coordinator"
    assert last_command["success"] is True
    assert last_command["reason"] == "target reached"
