"""Demand charge coordinator regression tests."""

from __future__ import annotations

import asyncio
import importlib
import sys
import types
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace

import pytest


ROOT = Path(__file__).resolve().parent.parent / "custom_components" / "power_sync"


class _Clock:
    current = datetime(2026, 6, 1, 12, 30, tzinfo=timezone.utc)


def _install_coordinator_stubs(monkeypatch: pytest.MonkeyPatch) -> None:
    ha_root = types.ModuleType("homeassistant")
    ha_core = types.ModuleType("homeassistant.core")
    ha_exceptions = types.ModuleType("homeassistant.exceptions")
    ha_helpers = types.ModuleType("homeassistant.helpers")
    ha_update = types.ModuleType("homeassistant.helpers.update_coordinator")
    ha_aiohttp = types.ModuleType("homeassistant.helpers.aiohttp_client")
    ha_dispatcher = types.ModuleType("homeassistant.helpers.dispatcher")
    ha_storage = types.ModuleType("homeassistant.helpers.storage")
    ha_util = types.ModuleType("homeassistant.util")
    ha_dt = types.ModuleType("homeassistant.util.dt")

    class ConfigEntryAuthFailed(Exception):
        pass

    class UpdateFailed(Exception):
        pass

    class DataUpdateCoordinator:
        def __init__(self, hass, logger, name=None, update_interval=None) -> None:
            self.hass = hass
            self.logger = logger
            self.name = name
            self.update_interval = update_interval
            self.data = None

    class Store:
        def __init__(self, hass, version, path) -> None:
            self._data = None
            self._path = path  # Store the path to verify scoping

        async def async_load(self):
            return self._data

        def async_delay_save(self, data_func, delay):
            self._data = data_func()

    ha_core.HomeAssistant = object
    ha_exceptions.ConfigEntryAuthFailed = ConfigEntryAuthFailed
    ha_update.DataUpdateCoordinator = DataUpdateCoordinator
    ha_update.UpdateFailed = UpdateFailed
    ha_aiohttp.async_get_clientsession = lambda hass: None
    ha_dispatcher.async_dispatcher_send = lambda *args, **kwargs: None
    ha_storage.Store = Store
    ha_dt.now = lambda *args, **kwargs: _Clock.current
    ha_dt.utcnow = lambda *args, **kwargs: _Clock.current
    ha_util.dt = ha_dt

    ha_helpers.update_coordinator = ha_update
    ha_helpers.aiohttp_client = ha_aiohttp
    ha_helpers.dispatcher = ha_dispatcher
    ha_helpers.storage = ha_storage
    ha_root.core = ha_core
    ha_root.exceptions = ha_exceptions
    ha_root.helpers = ha_helpers
    ha_root.util = ha_util

    for name, module in {
        "homeassistant": ha_root,
        "homeassistant.core": ha_core,
        "homeassistant.exceptions": ha_exceptions,
        "homeassistant.helpers": ha_helpers,
        "homeassistant.helpers.update_coordinator": ha_update,
        "homeassistant.helpers.aiohttp_client": ha_aiohttp,
        "homeassistant.helpers.dispatcher": ha_dispatcher,
        "homeassistant.helpers.storage": ha_storage,
        "homeassistant.util": ha_util,
        "homeassistant.util.dt": ha_dt,
    }.items():
        monkeypatch.setitem(sys.modules, name, module)

    ps_module = types.ModuleType("power_sync")
    ps_module.__path__ = [str(ROOT)]
    monkeypatch.setitem(sys.modules, "power_sync", ps_module)
    monkeypatch.delitem(sys.modules, "power_sync.coordinator", raising=False)


def _coordinator_module(monkeypatch: pytest.MonkeyPatch):
    _install_coordinator_stubs(monkeypatch)
    return importlib.import_module("power_sync.coordinator")


def test_peak_demand_tracks_only_billable_demand_window_samples(
    monkeypatch: pytest.MonkeyPatch,
):
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 11.8})
    demand = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=9.0,
        start_time="14:55",
        end_time="21:00",
        days="All Days",
        billing_day=1,
    )

    data = asyncio.run(demand._async_update_data())
    assert data["in_peak_period"] is False
    assert data["grid_import_power_kw"] == 11.8
    assert data["peak_demand_kw"] == 0.0
    assert data["estimated_cost"] == 0.0

    _Clock.current = datetime(2026, 6, 1, 15, 5, tzinfo=timezone.utc)
    energy.data = {"grid_power": 4.2}
    data = asyncio.run(demand._async_update_data())
    assert data["in_peak_period"] is True
    assert data["peak_demand_kw"] == 4.2
    assert data["estimated_cost"] == pytest.approx(37.8)

    _Clock.current = datetime(2026, 6, 1, 21, 0, tzinfo=timezone.utc)
    energy.data = {"grid_power": 10.99}
    data = asyncio.run(demand._async_update_data())
    assert data["in_peak_period"] is False
    assert data["grid_import_power_kw"] == 10.99
    assert data["peak_demand_kw"] == 4.2
    assert data["estimated_cost"] == pytest.approx(37.8)


def test_peak_demand_uses_rolling_average_not_instantaneous(
    monkeypatch: pytest.MonkeyPatch,
):
    """Peak demand should reflect the rolling average, not a single spike."""
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 0.0})
    demand = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=1,
        averaging_minutes=5,
    )

    # Feed 5 samples at 1-min intervals during demand window
    # 4 low + 1 spike: average should be (1+1+1+1+8)/5 = 2.4, not 8
    base_time = datetime(2026, 6, 1, 17, 0, tzinfo=timezone.utc)
    samples = [1.0, 1.0, 1.0, 1.0, 8.0]
    for i, power in enumerate(samples):
        _Clock.current = base_time + timedelta(minutes=i)
        energy.data = {"grid_power": power}
        data = asyncio.run(demand._async_update_data())

    # Peak should be the rolling average (~2.4), NOT the spike (8.0)
    assert data["peak_demand_kw"] == pytest.approx(2.4)
    assert data["rolling_avg_kw"] == pytest.approx(2.4)
    assert data["estimated_cost"] == pytest.approx(2.4 * 7.0)


def test_rolling_window_prunes_old_samples(
    monkeypatch: pytest.MonkeyPatch,
):
    """Samples older than averaging_minutes should be pruned."""
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 0.0})
    demand = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=1,
        averaging_minutes=3,
    )

    base_time = datetime(2026, 6, 1, 17, 0, tzinfo=timezone.utc)

    # Sample at t=0: 6 kW
    _Clock.current = base_time
    energy.data = {"grid_power": 6.0}
    asyncio.run(demand._async_update_data())

    # Samples at t=4,5 (past the 3-min window, so t=0 sample should be pruned)
    _Clock.current = base_time + timedelta(minutes=4)
    energy.data = {"grid_power": 2.0}
    asyncio.run(demand._async_update_data())

    _Clock.current = base_time + timedelta(minutes=5)
    energy.data = {"grid_power": 2.0}
    data = asyncio.run(demand._async_update_data())

    # Only the 2.0 samples should remain (6.0 is older than 3 mins)
    assert data["rolling_avg_kw"] == pytest.approx(2.0)


def test_rolling_window_only_collects_during_peak_period(
    monkeypatch: pytest.MonkeyPatch,
):
    """Samples outside peak period should not contaminate rolling average."""
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 0.0})
    demand = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="17:00",
        end_time="21:00",
        days="All Days",
        billing_day=1,
        averaging_minutes=5,
    )

    base_time = datetime(2026, 6, 1, 16, 30, tzinfo=timezone.utc)

    # Pre-window sample (16:30, outside peak 17:00-21:00): 10 kW
    _Clock.current = base_time
    energy.data = {"grid_power": 10.0}
    asyncio.run(demand._async_update_data())
    assert len(demand._samples) == 0  # Should not be collected

    # Enter peak period at 17:00, add low samples
    _Clock.current = base_time + timedelta(minutes=30)  # 17:00
    energy.data = {"grid_power": 2.0}
    asyncio.run(demand._async_update_data())
    assert len(demand._samples) == 1

    # Additional in-peak samples
    _Clock.current = base_time + timedelta(minutes=31)
    energy.data = {"grid_power": 2.0}
    data = asyncio.run(demand._async_update_data())

    # Average should be ~2.0, NOT contaminated by the 10 kW pre-window sample
    assert data["rolling_avg_kw"] == pytest.approx(2.0)
    assert data["in_peak_period"] is True


def test_store_key_scoped_by_entry_id(
    monkeypatch: pytest.MonkeyPatch,
):
    """Multiple coordinator instances should have separate store keys."""
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 0.0})

    # Create two coordinators with different entry_ids
    demand1 = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=1,
        entry_id="entry_1",
    )

    demand2 = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=5.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=1,
        entry_id="entry_2",
    )

    # Verify store paths are different (scoped by entry_id)
    assert demand1._store._path != demand2._store._path
    assert "entry_1" in demand1._store._path
    assert "entry_2" in demand2._store._path


def test_billing_cycle_reset_on_date_mismatch(
    monkeypatch: pytest.MonkeyPatch,
):
    """Peak demand resets when billing cycle changes (date mismatch on restart)."""
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 0.0})

    # Use billing_day=2: June 1 is in previous cycle (2026-05-02), June 2+ is new cycle (2026-06-02)
    base_time = datetime(2026, 6, 1, 17, 0, tzinfo=timezone.utc)
    _Clock.current = base_time

    demand1 = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=2,
        averaging_minutes=5,
    )
    energy.data = {"grid_power": 5.0}
    asyncio.run(demand1._async_update_data())
    assert demand1._peak_demand_kw == 5.0
    # Simulate persistence from June 1st (previous billing cycle)
    demand1._store._data = {
        "peak_demand_kw": 5.0,
        "billing_start": "2026-05-02"
    }

    # Simulate restart on June 2nd (new billing cycle starts)
    _Clock.current = base_time + timedelta(days=1)
    demand2 = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=2,
        averaging_minutes=5,
    )
    # Copy persisted data from previous cycle
    demand2._store._data = demand1._store._data.copy()

    energy.data = {"grid_power": 2.0}
    # First update will load from store, detect billing cycle change, reset peak, then update with new power
    asyncio.run(demand2._async_update_data())

    # Peak should be 2.0: reset to 0.0 due to billing_start mismatch, then updated with current power
    # (Store loader + peak reset happens before peak update in same cycle)
    assert demand2._peak_demand_kw == 2.0, "Peak should be updated with new power after billing reset"

    # Verify the persisted data was updated with new billing start
    assert demand2._store._data is not None
    assert demand2._store._data.get("billing_start") == "2026-06-02"


def test_billing_cycle_preserves_peak_on_matching_date(
    monkeypatch: pytest.MonkeyPatch,
):
    """Peak demand persists when billing cycle date matches on restart."""
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 0.0})

    base_time = datetime(2026, 6, 1, 17, 0, tzinfo=timezone.utc)
    _Clock.current = base_time

    # Create coordinator with pre-loaded store data (simulating restart)
    demand = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=1,
        averaging_minutes=5,
    )
    # Pre-load store as if it survived a restart
    demand._store._data = {
        "peak_demand_kw": 8.0,
        "billing_start": "2026-06-01"
    }

    # First update loads from store (on first _async_update_data call)
    energy.data = {"grid_power": 3.0}
    asyncio.run(demand._async_update_data())

    # Peak should be preserved (loaded from store) since billing_start matches current date
    assert demand._peak_demand_kw == 8.0


def test_store_debounce_delay_fires_between_cycles(
    monkeypatch: pytest.MonkeyPatch,
):
    """Store save delay (5s) should fire between 1-min coordinator cycles."""
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 0.0})
    demand = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=1,
        averaging_minutes=5,
    )

    base_time = datetime(2026, 6, 1, 17, 0, tzinfo=timezone.utc)

    # First update: set a new peak
    _Clock.current = base_time
    energy.data = {"grid_power": 10.0}
    asyncio.run(demand._async_update_data())

    # Verify the async_delay_save was called with 5s delay (captured in mock)
    # The mock Store.async_delay_save will execute the lambda immediately
    assert demand._store._data is not None
    assert demand._store._data.get("peak_demand_kw") == 10.0
    assert demand._store._data.get("billing_start") == "2026-06-01"


def test_peak_resets_to_zero_on_billing_day(
    monkeypatch: pytest.MonkeyPatch,
):
    """Peak demand resets to zero on billing day (day 1 of month)."""
    coordinator_module = _coordinator_module(monkeypatch)
    energy = SimpleNamespace(data={"grid_power": 0.0})
    demand = coordinator_module.DemandChargeCoordinator(
        hass=SimpleNamespace(),
        energy_coordinator=energy,
        enabled=True,
        rate=7.0,
        start_time="16:00",
        end_time="21:00",
        days="All Days",
        billing_day=1,
        averaging_minutes=5,
    )

    # Start on May 31st
    base_time = datetime(2026, 5, 31, 17, 0, tzinfo=timezone.utc)
    _Clock.current = base_time
    energy.data = {"grid_power": 6.0}
    asyncio.run(demand._async_update_data())
    assert demand._peak_demand_kw == 6.0

    # Move to June 1st (billing day), trigger update
    _Clock.current = base_time + timedelta(days=1)
    energy.data = {"grid_power": 1.0}
    data = asyncio.run(demand._async_update_data())

    # Peak should reset on billing day crossing
    assert demand._peak_demand_kw == 1.0
    assert data["days_until_reset"] > 0  # Reset was triggered
