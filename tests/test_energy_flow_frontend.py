"""Regression tests for the built-in energy flow dashboard card."""

from __future__ import annotations

from pathlib import Path


ENERGY_FLOW_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "power_sync"
    / "frontend"
    / "power-sync-energy-flow.js"
)


def test_energy_flow_uses_webkit_safe_svg_image_and_scaling():
    source = ENERGY_FLOW_PATH.read_text()

    assert "xlink:href" in source
    assert "setAttributeNS(XLINK_NS, 'xlink:href', url)" in source
    assert "getAttributeNS(XLINK_NS, 'href')" in source
    assert "function scaledSceneViewBox(scale)" in source
    assert 'viewBox="${sceneViewBox}"' in source
    assert "transform: scale" not in source


def test_energy_flow_avoids_svg_filter_repaint_hotspots():
    source = ENERGY_FLOW_PATH.read_text()

    assert "drop-shadow" not in source
    assert "paint-order: stroke fill" in source
    assert "el.textContent !== value" in source
