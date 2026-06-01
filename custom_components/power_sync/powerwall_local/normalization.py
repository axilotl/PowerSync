"""Normalization helpers for Tesla Powerwall local readback values."""

from __future__ import annotations

from typing import Any


# Powerwall keeps a hidden low-SOE reserve. Local hardware/config values include
# that reserve, while Tesla app/cloud UI presents the user-facing reserve target.
LOW_SOE_RESERVE_PCT = 5.0


def normalize_local_soc_percent(value: Any) -> float | None:
    """Map raw full-pack SOE percent to Tesla app/cloud SOC percent."""
    try:
        raw_soc = float(value)
    except (TypeError, ValueError):
        return None
    raw_soc = max(0.0, min(100.0, raw_soc))
    return max(
        0.0,
        (raw_soc - LOW_SOE_RESERVE_PCT)
        / (100.0 - LOW_SOE_RESERVE_PCT)
        * 100.0,
    )


def normalize_local_backup_reserve_percent(value: Any) -> int | None:
    """Map local Powerwall backup reserve readback to the user-facing target."""
    try:
        local_reserve = float(value)
    except (TypeError, ValueError):
        return None
    if local_reserve >= 100:
        return 100
    if local_reserve <= LOW_SOE_RESERVE_PCT:
        return 0
    return int(
        round(
            max(0.0, min(100.0, local_reserve - LOW_SOE_RESERVE_PCT))
        )
    )


def local_backup_reserve_write_percent(value: Any) -> int | None:
    """Map a user-facing reserve target to the local Powerwall config value."""
    try:
        reserve = float(value)
    except (TypeError, ValueError):
        return None
    reserve = max(0.0, min(100.0, reserve))
    if reserve >= 100:
        return 100
    return int(
        round(
            max(0.0, min(100.0, reserve + LOW_SOE_RESERVE_PCT))
        )
    )
