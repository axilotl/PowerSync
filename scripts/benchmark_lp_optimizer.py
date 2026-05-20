#!/usr/bin/env python3
"""Opt-in benchmark for the built-in battery LP optimizer.

Run from the repository root:
    python scripts/benchmark_lp_optimizer.py
"""

from __future__ import annotations

import importlib
import statistics
import sys
import time
import types
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"


def _install_stubs() -> None:
    """Install minimal Home Assistant stubs for local optimizer benchmarking."""
    ha_root = types.ModuleType("homeassistant")
    ha_util = types.ModuleType("homeassistant.util")
    ha_dt = types.ModuleType("homeassistant.util.dt")
    ha_dt.now = lambda *args, **kwargs: datetime.now(timezone.utc)
    ha_dt.utcnow = lambda *args, **kwargs: datetime.now(timezone.utc)
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


def _run_case(name: str, optimizer_cls, kwargs: dict, runs: int = 3) -> None:
    elapsed: list[float] = []
    solver_times: list[float] = []
    periods: list[int] = []
    solvers: list[str] = []

    for _ in range(runs):
        optimizer = optimizer_cls(
            capacity_wh=13500,
            max_charge_w=7000,
            max_discharge_w=7000,
            backup_reserve=0.20,
            interval_minutes=5,
            horizon_hours=48,
        )
        start = time.monotonic()
        result = optimizer.optimize(**kwargs)
        elapsed.append(time.monotonic() - start)
        solver_times.append(result.lp_stats.get("solver_time_s", 0.0))
        periods.append(result.lp_stats.get("period_count", len(result.schedule.actions)))
        solvers.append(result.solver_used)

    print(
        f"{name:28s} total={statistics.median(elapsed):6.3f}s "
        f"solver={statistics.median(solver_times):6.3f}s "
        f"periods={int(statistics.median(periods)):4d} "
        f"solver_used={solvers[-1]}"
    )


def main() -> int:
    _install_stubs()
    module = importlib.import_module("power_sync.optimization.battery_optimizer")
    if not module.SCIPY_AVAILABLE:
        print("scipy is not available; LP benchmark cannot run")
        return 1

    n = 576
    cases = {
        "flat tariff": {
            "import_prices": [0.25] * n,
            "export_prices": [0.08] * n,
            "solar_forecast": [0.0] * n,
            "load_forecast": [0.7] * n,
            "current_soc": 0.50,
            "allow_battery_export": [False] * n,
        },
        "volatile tariff": {
            "import_prices": [0.08 if i % 12 < 4 else 0.35 for i in range(n)],
            "export_prices": [0.05 if i % 24 < 12 else 0.45 for i in range(n)],
            "solar_forecast": [0.0] * n,
            "load_forecast": [0.7] * n,
            "current_soc": 0.50,
            "allow_battery_export": [i % 24 >= 12 for i in range(n)],
        },
        "positive fit cheap import": {
            "import_prices": [0.069] * 202 + [0.2856] * (n - 202),
            "export_prices": [0.12] * n,
            "solar_forecast": [0.0] * n,
            "load_forecast": [0.7] * n,
            "current_soc": 0.19,
            "acquisition_cost_kwh": 0.0,
            "allow_battery_export": [True] * n,
        },
        "solar no grid charge": {
            "import_prices": [0.30] * n,
            "export_prices": [0.08] * n,
            "solar_forecast": [5.0 if 96 <= i < 192 else 0.0 for i in range(n)],
            "load_forecast": [0.5] * n,
            "current_soc": 0.20,
            "allow_battery_export": [False] * n,
            "allow_grid_charge": False,
        },
    }

    for name, kwargs in cases.items():
        _run_case(name, module.BatteryOptimizer, kwargs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
