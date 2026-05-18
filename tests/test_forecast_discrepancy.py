"""Tests for Amber forecast discrepancy detection."""

from __future__ import annotations

import importlib
import sys
import types
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"
_SENTINEL = object()


def _tariff_converter_module():
    saved_modules = {
        name: sys.modules.get(name, _SENTINEL)
        for name in (
            "power_sync",
            "power_sync.tariff_converter",
            "power_sync.currency",
            "homeassistant",
            "homeassistant.util",
            "homeassistant.util.dt",
        )
    }

    power_sync = types.ModuleType("power_sync")
    power_sync.__path__ = [str(COMPONENT_ROOT)]
    sys.modules["power_sync"] = power_sync
    ha_root = types.ModuleType("homeassistant")
    ha_util = types.ModuleType("homeassistant.util")
    ha_dt = types.ModuleType("homeassistant.util.dt")
    ha_util.dt = ha_dt
    ha_root.util = ha_util
    sys.modules["homeassistant"] = ha_root
    sys.modules["homeassistant.util"] = ha_util
    sys.modules["homeassistant.util.dt"] = ha_dt

    try:
        return importlib.import_module("power_sync.tariff_converter")
    finally:
        sys.modules.pop("power_sync.tariff_converter", None)
        for name, module in saved_modules.items():
            if module is _SENTINEL:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = module


def test_compare_forecast_types_uses_high_as_conservative_forecast():
    converter = _tariff_converter_module()

    result = converter.compare_forecast_types(
        [
            {
                "nemTime": "2026-05-18T00:30:00+10:00",
                "type": "ForecastInterval",
                "channelType": "general",
                "advancedPrice": {
                    "predicted": 40.0,
                    "low": 25.0,
                    "high": 55.0,
                },
            },
            {
                "nemTime": "2026-05-18T01:00:00+10:00",
                "type": "ForecastInterval",
                "channelType": "general",
                "advancedPrice": {
                    "predicted": 60.0,
                    "low": 30.0,
                    "high": 85.0,
                },
            },
        ],
        threshold=10.0,
    )

    assert result["has_discrepancy"] is True
    assert result["avg_difference"] == 20.0
    assert result["max_difference"] == 25.0
    assert result["samples"] == 2
    assert result["details"][0]["conservative"] == 85.0
