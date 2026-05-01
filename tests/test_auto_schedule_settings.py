"""Tests for auto-schedule settings serialization and clearing."""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent / "custom_components" / "power_sync"

sys.modules.setdefault("aiohttp", types.ModuleType("aiohttp"))

_ha_root = sys.modules.setdefault("homeassistant", types.ModuleType("homeassistant"))
_ha_util = sys.modules.setdefault("homeassistant.util", types.ModuleType("homeassistant.util"))
_ha_dt = sys.modules.setdefault("homeassistant.util.dt", types.ModuleType("homeassistant.util.dt"))
_ha_dt.now = getattr(_ha_dt, "now", lambda *args, **kwargs: None)
_ha_util.dt = _ha_dt
_ha_root.util = _ha_util

_ps = types.ModuleType("power_sync")
_ps.__path__ = [str(ROOT)]
sys.modules["power_sync"] = _ps

_automations = types.ModuleType("power_sync.automations")
_automations.__path__ = [str(ROOT / "automations")]
sys.modules["power_sync.automations"] = _automations

sys.modules.pop("power_sync.const", None)
ev_planner = importlib.import_module("power_sync.automations.ev_charging_planner")


def test_empty_departure_times_does_not_rehydrate_legacy_schedule():
    settings = ev_planner.AutoScheduleSettings.from_dict({
        "departure_time": "07:30",
        "departure_days": [0, 1, 2, 3, 4],
        "departure_times": {},
    })

    assert settings.departure_times == {}
    assert settings.to_dict()["departure_time"] is None
    assert settings.to_dict()["departure_days"] == []


def test_empty_per_day_overrides_clear_legacy_aliases():
    settings = ev_planner.AutoScheduleSettings.from_dict({
        "departure_priorities": {},
        "departure_min_battery_to_start": {},
        "departure_home_battery_min": {"0": 80},
        "departure_limit_grid_import": {},
        "departure_no_grid_import": {"0": True},
        "departure_consume_battery_level": {},
        "departure_stop_at_battery_floor": {},
    })

    assert settings.departure_priorities == {}
    assert settings.departure_min_battery_to_start == {}
    assert settings.departure_limit_grid_import == {}
    assert settings.departure_consume_battery_level == {}
    assert settings.departure_stop_at_battery_floor == {}
