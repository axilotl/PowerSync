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


def test_energy_flow_keeps_scene_bitmap_outside_animated_svg_layer():
    source = ENERGY_FLOW_PATH.read_text()

    assert 'id="flow-scene-frame"' in source
    assert "--scene-background" in source
    assert "cssBackgroundUrl(url)" in source
    assert "new Image()" in source
    assert '<image id="flow-scene-image"' not in source
    assert "xlink:href" not in source
    assert "function scaledSceneViewBox(scale)" in source
    assert 'viewBox="${sceneViewBox}"' in source
    assert "transform: scale" not in source


def test_energy_flow_avoids_svg_filter_repaint_hotspots():
    source = ENERGY_FLOW_PATH.read_text()

    assert "drop-shadow" not in source
    assert "paint-order: stroke fill" in source
    assert "el.textContent !== value" in source


def test_energy_flow_caps_dash_gap_for_short_active_paths():
    source = ENERGY_FLOW_PATH.read_text()

    assert "_syncFlowLineMetrics" in source
    assert "getTotalLength()" in source
    assert "Short SVG paths can fall entirely inside a long dash gap" in source
    assert "el.style.setProperty('--flow-seg'" in source
    assert "el.style.setProperty('--flow-gap'" in source
