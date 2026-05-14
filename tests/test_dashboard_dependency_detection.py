"""Regression tests for dashboard HACS dependency detection."""

from __future__ import annotations

from pathlib import Path


STRATEGY_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "power_sync"
    / "frontend"
    / "power-sync-strategy.js"
)


def test_button_card_resource_fallback_accepts_dashed_hacs_url():
    """button-card HACS URLs include dashes and must not be normalized away."""
    source = STRATEGY_PATH.read_text()

    assert "c.element," in source
    assert "c.hacs," in source
    assert "c.element.replace(/-/g, '')" in source
    assert "c.hacs?.replace(/-/g, '')" in source
    assert "url.includes(name)" in source


def test_optimizer_windows_use_combined_visual_card():
    """Charge and discharge windows should render as one dashboard schedule card."""
    source = STRATEGY_PATH.read_text()

    assert "optimization_force_charge_windows" in source
    assert "optimization_force_discharge_windows" in source
    assert "Planned Battery Windows" in source
    assert "ps-window-row" in source
    assert "Future Force Charge" not in source
