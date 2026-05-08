"""Tests for Zaptec Cloud state parsing."""

from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "power_sync"
    / "zaptec_api.py"
)
SPEC = importlib.util.spec_from_file_location("zaptec_api", MODULE_PATH)
zaptec_api = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(zaptec_api)


def test_parse_charger_state_uses_zaptec_observation_ids():
    client = zaptec_api.ZaptecCloudClient("user@example.com", "password")

    parsed = client.parse_charger_state(
        {
            120: "1",
            151: "true",
            507: "6.1",
            508: "7.2",
            509: "8.3",
            520: "99",
            521: "98",
            522: "97",
            553: "1.25",
            710: "3",
            911: "1.2.3",
        }
    )

    assert parsed["charger_operation_mode"] == "charging"
    assert parsed["cable_locked"] is True
    assert parsed["permanent_cable_lock"] is True
    assert parsed["session_energy_wh"] == 1250
    assert parsed["phase_a_current"] == 6.1
    assert parsed["phase_b_current"] == 7.2
    assert parsed["phase_c_current"] == 8.3
    assert parsed["firmware_version"] == "1.2.3"
