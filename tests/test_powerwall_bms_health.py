"""Tests for Tesla Powerwall BMS health normalisation."""

from __future__ import annotations

import importlib.util
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "custom_components"
    / "power_sync"
    / "powerwall_local"
    / "bms_health.py"
)
SPEC = importlib.util.spec_from_file_location("powerwall_bms_health", MODULE_PATH)
assert SPEC and SPEC.loader
bms_health = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(bms_health)
reconcile_pack_remaining_with_aggregate = (
    bms_health.reconcile_pack_remaining_with_aggregate
)


def test_reconciles_serial_less_near_empty_expansion_from_aggregate_remaining():
    packs = [
        {
            "role": "leader",
            "serialNumber": "LEADER",
            "isExpansion": False,
            "nominalFullPackEnergyWh": 14290.0,
            "nominalEnergyRemainingWh": 5740.0,
        },
        {
            "role": "follower",
            "serialNumber": "FOLLOWER",
            "isExpansion": False,
            "nominalFullPackEnergyWh": 14290.0,
            "nominalEnergyRemainingWh": 6820.0,
        },
        {
            "role": "expansion",
            "serialNumber": "EXPANSION",
            "isExpansion": True,
            "nominalFullPackEnergyWh": 14420.0,
            "nominalEnergyRemainingWh": 6950.0,
        },
        {
            "role": "expansion",
            "serialNumber": None,
            "isExpansion": True,
            "nominalFullPackEnergyWh": 14470.0,
            "nominalEnergyRemainingWh": 200.0,
        },
    ]

    result = reconcile_pack_remaining_with_aggregate(packs, 25750.0, 57400.0)

    corrected = result[3]
    assert corrected["rawNominalEnergyRemainingWh"] == 200.0
    assert corrected["remainingReconciledFromAggregate"] is True
    assert corrected["nominalEnergyRemainingWh"] == 6240.0
    assert sum(pack["nominalEnergyRemainingWh"] for pack in result) == 25750.0


def test_does_not_reconcile_when_pack_sum_already_matches_aggregate():
    packs = [
        {
            "role": "leader",
            "serialNumber": "LEADER",
            "isExpansion": False,
            "nominalFullPackEnergyWh": 14290.0,
            "nominalEnergyRemainingWh": 5740.0,
        },
        {
            "role": "expansion",
            "serialNumber": None,
            "isExpansion": True,
            "nominalFullPackEnergyWh": 14470.0,
            "nominalEnergyRemainingWh": 200.0,
        },
    ]

    result = reconcile_pack_remaining_with_aggregate(packs, 5940.0, 28760.0)

    assert result[1]["nominalEnergyRemainingWh"] == 200.0
    assert "remainingReconciledFromAggregate" not in result[1]


def test_does_not_reconcile_when_pack_capacities_do_not_match_aggregate():
    packs = [
        {
            "role": "leader",
            "serialNumber": "LEADER",
            "isExpansion": False,
            "nominalFullPackEnergyWh": 14290.0,
            "nominalEnergyRemainingWh": 5740.0,
        },
        {
            "role": "expansion",
            "serialNumber": None,
            "isExpansion": True,
            "nominalFullPackEnergyWh": 14470.0,
            "nominalEnergyRemainingWh": 200.0,
        },
    ]

    result = reconcile_pack_remaining_with_aggregate(packs, 12000.0, 43000.0)

    assert result[1]["nominalEnergyRemainingWh"] == 200.0
    assert "remainingReconciledFromAggregate" not in result[1]
