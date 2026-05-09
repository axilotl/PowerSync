"""Regression tests for automation state coordinator discovery."""

from __future__ import annotations

import ast
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
AUTOMATIONS_PATH = ROOT / "custom_components" / "power_sync" / "automations" / "__init__.py"


def test_automation_current_state_includes_supported_battery_coordinators():
    tree = ast.parse(AUTOMATIONS_PATH.read_text())
    method = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.AsyncFunctionDef)
        and node.name == "_async_get_current_state"
    )
    source = ast.get_source_segment(AUTOMATIONS_PATH.read_text(), method)

    for coordinator_key in (
        "tesla_coordinator",
        "sigenergy_coordinator",
        "sungrow_coordinator",
        "foxess_coordinator",
        "goodwe_coordinator",
        "alphaess_coordinator",
        "solax_coordinator",
        "esy_coordinator",
        "saj_h2_coordinator",
        "neovolt_coordinator",
    ):
        assert coordinator_key in source
