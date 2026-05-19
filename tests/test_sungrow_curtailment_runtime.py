"""Regression coverage for Sungrow export-limit curtailment routing."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
INIT_PATH = ROOT / "custom_components" / "power_sync" / "__init__.py"


def _function_source(name: str) -> str:
    source = INIT_PATH.read_text()
    module = ast.parse(source)
    for node in module.body:
        if isinstance(node, ast.AsyncFunctionDef) and node.name == "async_setup_entry":
            for child in node.body:
                if isinstance(child, ast.AsyncFunctionDef) and child.name == name:
                    segment = ast.get_source_segment(source, child)
                    assert segment is not None
                    return segment
    raise AssertionError(f"{name} not found")


def test_sungrow_has_native_export_limit_curtailment_handler():
    handler = _function_source("handle_sungrow_curtailment")

    assert "sungrow_curtailment_state" in handler
    assert "sungrow_power_limit_w" in handler
    assert "await sungrow_coord.set_export_limit(home_load_w)" in handler
    assert "await sungrow_coord.set_export_limit(None)" in handler
    assert "ac_inverter_is_same_hybrid" in handler
    assert "await apply_inverter_curtailment(" in handler


def test_periodic_solar_curtailment_routes_to_sungrow_before_tesla_path():
    handler = _function_source("handle_solar_curtailment_check")
    pre_tesla_path = handler[: handler.index("if token_getter is None:")]

    assert "if is_sungrow:" in pre_tesla_path
    assert "await handle_sungrow_curtailment()" in pre_tesla_path


def test_websocket_solar_curtailment_routes_to_sungrow_with_prices():
    handler = _function_source("handle_solar_curtailment_with_websocket_data")
    pre_tesla_path = handler[: handler.index("if token_getter is None:")]

    assert "if is_sungrow:" in pre_tesla_path
    assert (
        "await handle_sungrow_curtailment("
        "feedin_price=feedin_price, import_price=import_price)"
    ) in pre_tesla_path
