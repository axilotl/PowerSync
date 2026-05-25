"""Regression tests for Flow Power pricing inputs."""

from __future__ import annotations

import ast
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
COMPONENT_ROOT = ROOT / "custom_components" / "power_sync"


def _method_source(file_path: Path, class_name: str, method_name: str) -> str:
    module = ast.parse(file_path.read_text())
    for node in module.body:
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == method_name:
                    return ast.unparse(item)
    raise AssertionError(f"{class_name}.{method_name} not found")


def test_flow_power_uses_raw_wholesale_twap_not_portal_twap_for_sensor_pricing():
    source = _method_source(
        COMPONENT_ROOT / "sensor.py",
        "FlowPowerPriceSensor",
        "_get_effective_twap",
    )

    assert "flow_power_portal_data" not in source
    assert "_get_market_avg" in source


def test_flow_power_tariff_generation_does_not_substitute_portal_twap():
    source = (COMPONENT_ROOT / "__init__.py").read_text()

    assert "Using portal TWAP" not in source
    assert 'portal_data["twap"]' not in source


def test_flow_power_twap_sample_is_recorded_before_battery_route_returns():
    source = (COMPONENT_ROOT / "__init__.py").read_text()
    sample_call = "_record_flow_power_twap_sample(electricity_provider, general_price)"
    route_marker = "# Route to appropriate battery system for tariff sync"

    assert source.index(sample_call) < source.index(route_marker)
    assert source.count("record_price(") == 1


def test_power_sync_requires_aemo_to_tariff_with_endeavour_n73():
    manifest = json.loads((COMPONENT_ROOT / "manifest.json").read_text())

    assert "aemo-to-tariff>=0.7.15" in manifest["requirements"]
