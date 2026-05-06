"""Regression tests for Sigenergy tariff conversion."""

from __future__ import annotations

import importlib
import sys
import types
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"
_SENTINEL = object()


@pytest.fixture()
def sigenergy_api_module():
    saved_modules = {
        name: sys.modules.get(name, _SENTINEL)
        for name in ("power_sync", "power_sync.sigenergy_api", "power_sync.const")
    }

    power_sync = types.ModuleType("power_sync")
    power_sync.__path__ = [str(COMPONENT_ROOT)]
    sys.modules["power_sync"] = power_sync

    try:
        yield importlib.import_module("power_sync.sigenergy_api")
    finally:
        sys.modules.pop("power_sync.sigenergy_api", None)
        for name, module in saved_modules.items():
            if module is _SENTINEL:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


def _interval(ts: datetime, price: float, channel: str = "general") -> dict:
    return {
        "nemTime": ts.isoformat(),
        "duration": 30,
        "type": "ForecastInterval",
        "channelType": channel,
        "advancedPrice": {"predicted": price},
        "perKwh": price,
    }


def test_sigenergy_converter_prefers_next_24h_date_for_past_clock_slots(
    sigenergy_api_module,
    monkeypatch,
):
    brisbane = ZoneInfo("Australia/Brisbane")

    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 5, 6, 20, 10, tzinfo=brisbane).astimezone(tz)

    monkeypatch.setattr(sigenergy_api_module, "datetime", FixedDatetime)

    today_midnight = datetime(2026, 5, 6, 0, 30, tzinfo=brisbane)
    tomorrow_midnight = datetime(2026, 5, 7, 0, 30, tzinfo=brisbane)
    current = datetime(2026, 5, 6, 20, 30, tzinfo=brisbane)

    prices = [
        _interval(today_midnight, 99.0),
        _interval(tomorrow_midnight, 12.0),
        _interval(current, 35.0),
    ]

    converted = sigenergy_api_module.convert_amber_prices_to_sigenergy(
        prices,
        price_type="buy",
        forecast_type="predicted",
        nem_region="QLD1",
    )

    by_start = {slot["timeRange"].split("-")[0]: slot["price"] for slot in converted}

    assert by_start["00:00"] == 12.0
    assert by_start["20:00"] == 35.0


def test_sigenergy_converter_does_not_average_multiple_dates_for_same_slot(
    sigenergy_api_module,
    monkeypatch,
):
    brisbane = ZoneInfo("Australia/Brisbane")

    class FixedDatetime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2026, 5, 6, 19, 40, tzinfo=brisbane).astimezone(tz)

    monkeypatch.setattr(sigenergy_api_module, "datetime", FixedDatetime)

    today_slot = datetime(2026, 5, 6, 21, 30, tzinfo=brisbane)
    tomorrow_slot = today_slot + timedelta(days=1)

    prices = [
        _interval(today_slot, 40.0),
        _interval(tomorrow_slot, 10.0),
    ]

    converted = sigenergy_api_module.convert_amber_prices_to_sigenergy(
        prices,
        price_type="buy",
        forecast_type="predicted",
        nem_region="QLD1",
    )

    by_start = {slot["timeRange"].split("-")[0]: slot["price"] for slot in converted}

    assert by_start["21:00"] == 40.0
