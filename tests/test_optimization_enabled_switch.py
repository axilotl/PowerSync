"""Regression tests for the Smart Optimization configuration switch."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONST_PATH = ROOT / "custom_components" / "power_sync" / "const.py"
SWITCH_PATH = ROOT / "custom_components" / "power_sync" / "switch.py"


def test_optimization_enabled_switch_is_registered_as_config_entity():
    const_source = CONST_PATH.read_text()
    switch_source = SWITCH_PATH.read_text()

    assert 'SWITCH_TYPE_OPTIMIZATION_ENABLED = "optimization_enabled"' in const_source
    assert "OptimizationEnabledSwitch(" in switch_source
    assert "key=SWITCH_TYPE_OPTIMIZATION_ENABLED" in switch_source
    assert 'name="Enable Smart Optimization"' in switch_source
    assert "class OptimizationEnabledSwitch(SwitchEntity):" in switch_source
    assert "_attr_entity_category = EntityCategory.CONFIG" in switch_source


def test_optimization_enabled_switch_persists_provider_and_enabled_flag():
    switch_source = SWITCH_PATH.read_text()

    assert "new_data[CONF_OPTIMIZATION_PROVIDER] = OPT_PROVIDER_POWERSYNC" in switch_source
    assert "new_options[CONF_OPTIMIZATION_PROVIDER] = OPT_PROVIDER_POWERSYNC" in switch_source
    assert "new_options[CONF_OPTIMIZATION_ENABLED] = True" in switch_source
    assert "new_options[CONF_OPTIMIZATION_ENABLED] = False" in switch_source
