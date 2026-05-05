"""Regression tests for battery-to-grid export gating."""

from __future__ import annotations

import importlib
import sys
import types
from datetime import datetime, timezone
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"

_SENTINEL = object()

_STUB_MODULE_NAMES = (
    "homeassistant",
    "homeassistant.util",
    "homeassistant.util.dt",
    "power_sync",
    "power_sync.optimization",
    "power_sync.optimization.battery_optimizer",
    "power_sync.optimization.schedule_reader",
)


def _install_stubs() -> None:
    ha_root = types.ModuleType("homeassistant")
    ha_util = types.ModuleType("homeassistant.util")
    ha_dt = types.ModuleType("homeassistant.util.dt")
    ha_dt.now = lambda *args, **kwargs: datetime(2026, 5, 4, 0, 0, tzinfo=timezone.utc)
    ha_dt.utcnow = lambda *args, **kwargs: datetime(2026, 5, 4, 0, 0, tzinfo=timezone.utc)
    ha_dt.UTC = timezone.utc
    ha_util.dt = ha_dt
    ha_root.util = ha_util

    sys.modules["homeassistant"] = ha_root
    sys.modules["homeassistant.util"] = ha_util
    sys.modules["homeassistant.util.dt"] = ha_dt

    ps_module = types.ModuleType("power_sync")
    ps_module.__path__ = [str(COMPONENT_ROOT)]
    sys.modules["power_sync"] = ps_module

    optimization_module = types.ModuleType("power_sync.optimization")
    optimization_module.__path__ = [str(COMPONENT_ROOT / "optimization")]
    sys.modules["power_sync.optimization"] = optimization_module


@pytest.fixture()
def battery_optimizer_module():
    saved_modules = {
        name: sys.modules.get(name, _SENTINEL)
        for name in _STUB_MODULE_NAMES
    }
    for name in _STUB_MODULE_NAMES:
        sys.modules.pop(name, None)

    _install_stubs()
    module = importlib.import_module("power_sync.optimization.battery_optimizer")
    try:
        yield module
    finally:
        for name in _STUB_MODULE_NAMES:
            if saved_modules[name] is _SENTINEL:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = saved_modules[name]


def _optimizer(module):
    return module.BatteryOptimizer(
        capacity_wh=13500,
        max_charge_w=7000,
        max_discharge_w=7000,
        backup_reserve=0.05,
        interval_minutes=5,
        horizon_hours=1,
    )


def test_default_blocks_battery_export_when_fit_beats_import(battery_optimizer_module):
    optimizer = _optimizer(battery_optimizer_module)

    result = optimizer.optimize(
        import_prices=[0.069] * 12,
        export_prices=[0.12] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.5] * 12,
        current_soc=0.80,
        acquisition_cost_kwh=0.0,
    )

    assert max(result.grid_export_w) <= 1e-6
    assert all(action.action != "export" for action in result.schedule.actions)
    assert max(action.battery_discharge_w for action in result.schedule.actions) <= 500.1


def test_explicit_battery_export_true_allows_export_when_profitable(
    battery_optimizer_module,
):
    optimizer = _optimizer(battery_optimizer_module)

    result = optimizer.optimize(
        import_prices=[0.05] * 12,
        export_prices=[0.50] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.1] * 12,
        current_soc=0.80,
        acquisition_cost_kwh=0.0,
        allow_battery_export=True,
    )

    assert max(result.grid_export_w) > 100.0
    assert any(action.action == "export" for action in result.schedule.actions)


def test_solar_surplus_export_still_works_when_battery_export_blocked(
    battery_optimizer_module,
):
    optimizer = _optimizer(battery_optimizer_module)

    result = optimizer.optimize(
        import_prices=[0.069] * 12,
        export_prices=[0.12] * 12,
        solar_forecast=[2.0] * 12,
        load_forecast=[0.5] * 12,
        current_soc=1.0,
        acquisition_cost_kwh=0.0,
        allow_battery_export=False,
    )

    assert min(result.grid_export_w) >= 1499.0
    assert max(result.grid_export_w) <= 1500.1
    assert all(action.action != "export" for action in result.schedule.actions)


def test_grid_export_cannot_come_from_grid_passthrough(battery_optimizer_module):
    optimizer = _optimizer(battery_optimizer_module)

    result = optimizer.optimize(
        import_prices=[0.05] * 12,
        export_prices=[0.50] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.0] * 12,
        current_soc=0.05,
        acquisition_cost_kwh=0.0,
        allow_battery_export=True,
    )

    assert max(result.grid_export_w) <= 1e-6
    assert max(result.grid_import_w) <= 1e-6


def test_below_reserve_can_grid_charge_during_cheap_window(battery_optimizer_module):
    optimizer = battery_optimizer_module.BatteryOptimizer(
        capacity_wh=13500,
        max_charge_w=5000,
        max_discharge_w=5000,
        backup_reserve=0.20,
        interval_minutes=5,
        horizon_hours=3,
    )

    result = optimizer.optimize(
        import_prices=[0.08] * 12 + [0.30] * 24,
        export_prices=[0.05] * 36,
        solar_forecast=[0.0] * 36,
        load_forecast=[1.0] * 36,
        current_soc=0.0,
        acquisition_cost_kwh=0.0,
        allow_battery_export=[False] * 36,
    )

    cheap_window = result.schedule.actions[:12]
    assert any(action.action == "charge" for action in cheap_window)
    assert max(action.battery_charge_w for action in cheap_window) > 1000


def test_battery_export_mask_allows_only_explicit_slots(battery_optimizer_module):
    optimizer = _optimizer(battery_optimizer_module)

    result = optimizer.optimize(
        import_prices=[0.05] * 12,
        export_prices=[0.50] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.1] * 12,
        current_soc=0.80,
        acquisition_cost_kwh=0.0,
        allow_battery_export=[False] * 6 + [True] * 6,
    )

    assert max(result.grid_export_w[:6]) <= 1e-6
    assert max(result.grid_export_w[6:]) > 100.0
    assert all(action.action != "export" for action in result.schedule.actions[:6])
    assert any(action.action == "export" for action in result.schedule.actions[6:])


def test_charge_block_mask_prevents_charging_during_export_window(
    battery_optimizer_module,
):
    optimizer = _optimizer(battery_optimizer_module)

    unblocked = optimizer.optimize(
        import_prices=[0.05] * 12,
        export_prices=[0.04] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.1] * 12,
        current_soc=0.20,
        acquisition_cost_kwh=0.0,
        allow_battery_export=[True] * 12,
        block_battery_charge=[False] * 12,
    )
    blocked = optimizer.optimize(
        import_prices=[0.05] * 12,
        export_prices=[0.50] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.1] * 12,
        current_soc=0.20,
        acquisition_cost_kwh=0.0,
        allow_battery_export=[True] * 12,
        block_battery_charge=[True] * 12,
    )

    assert max(action.battery_charge_w for action in unblocked.schedule.actions) > 100
    assert max(action.battery_charge_w for action in blocked.schedule.actions) <= 1e-6
    assert all(action.action != "charge" for action in blocked.schedule.actions)


def test_charge_block_mask_prevents_greedy_fallback_charging(
    battery_optimizer_module,
    monkeypatch,
):
    monkeypatch.setattr(battery_optimizer_module, "SCIPY_AVAILABLE", False)
    optimizer = _optimizer(battery_optimizer_module)

    unblocked = optimizer.optimize(
        import_prices=[0.05] * 12,
        export_prices=[0.04] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.1] * 12,
        current_soc=0.20,
        acquisition_cost_kwh=0.0,
        allow_battery_export=[True] * 12,
        block_battery_charge=[False] * 12,
    )
    blocked = optimizer.optimize(
        import_prices=[0.05] * 12,
        export_prices=[0.04] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.1] * 12,
        current_soc=0.20,
        acquisition_cost_kwh=0.0,
        allow_battery_export=[True] * 12,
        block_battery_charge=[True] * 12,
    )

    assert max(action.battery_charge_w for action in unblocked.schedule.actions) > 100
    assert max(action.battery_charge_w for action in blocked.schedule.actions) <= 1e-6
    assert all(action.action != "charge" for action in blocked.schedule.actions)


def test_charge_block_mask_overrides_free_import_force_charge(
    battery_optimizer_module,
):
    optimizer = _optimizer(battery_optimizer_module)

    unblocked = optimizer.optimize(
        import_prices=[0.0] * 12,
        export_prices=[0.0] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.1] * 12,
        current_soc=0.20,
        acquisition_cost_kwh=0.0,
        allow_battery_export=[True] * 12,
        block_battery_charge=[False] * 12,
    )
    blocked = optimizer.optimize(
        import_prices=[0.0] * 12,
        export_prices=[0.0] * 12,
        solar_forecast=[0.0] * 12,
        load_forecast=[0.1] * 12,
        current_soc=0.20,
        acquisition_cost_kwh=0.0,
        allow_battery_export=[True] * 12,
        block_battery_charge=[True] * 12,
    )

    assert any(action.action == "charge" for action in unblocked.schedule.actions)
    assert max(action.battery_charge_w for action in blocked.schedule.actions) <= 1e-6
    assert all(action.action != "charge" for action in blocked.schedule.actions)
