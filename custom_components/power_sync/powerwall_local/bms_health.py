"""Helpers for normalising Tesla Powerwall BMS health telemetry."""

from __future__ import annotations

import logging
from typing import Any


def _as_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def reconcile_pack_remaining_with_aggregate(
    packs: list[dict[str, Any]],
    aggregate_remaining_wh: Any,
    aggregate_full_wh: Any = None,
    *,
    logger: logging.Logger | None = None,
) -> list[dict[str, Any]]:
    """Fix stale near-empty expansion-pack readings using Tesla's aggregate BMS total.

    Tesla's MSA component surface can report a real expansion pack with a plausible
    full capacity but a stale near-zero remaining-energy value and no serial number.
    The control.systemStatus aggregate remains authoritative for the whole site, so
    use it to fill those suspect modules when all pack capacities are accounted for.
    """
    total_remaining = _as_float(aggregate_remaining_wh)
    if not packs or total_remaining is None or total_remaining <= 0:
        return packs

    prepared: list[tuple[dict[str, Any], float, float]] = []
    for pack in packs:
        full = _as_float(pack.get("nominalFullPackEnergyWh"))
        remaining = _as_float(pack.get("nominalEnergyRemainingWh"))
        if full is None or full <= 0 or remaining is None:
            return packs
        prepared.append((pack, full, remaining))

    pack_full_total = sum(full for _, full, _ in prepared)
    total_full = _as_float(aggregate_full_wh)
    if total_full and total_full > 0:
        full_tolerance = max(1000.0, total_full * 0.05)
        if abs(pack_full_total - total_full) > full_tolerance:
            return packs

    pack_remaining_total = sum(remaining for _, _, remaining in prepared)
    delta = total_remaining - pack_remaining_total
    remaining_tolerance = max(500.0, total_remaining * 0.05)
    if delta <= remaining_tolerance:
        return packs

    candidates: list[tuple[dict[str, Any], float, float]] = []
    for pack, full, remaining in prepared:
        is_expansion = bool(pack.get("isExpansion") or pack.get("role") == "expansion")
        has_serial = bool(pack.get("serialNumber") or pack.get("serial_number"))
        near_empty = remaining < 500.0 or remaining / full < 0.05
        if is_expansion and not has_serial and near_empty:
            candidates.append((pack, full, remaining))

    if not candidates:
        return packs

    candidate_ids = {id(pack) for pack, _, _ in candidates}
    trusted_remaining = sum(
        remaining
        for pack, _, remaining in prepared
        if id(pack) not in candidate_ids
    )
    replacement_remaining = total_remaining - trusted_remaining
    candidate_full_total = sum(full for _, full, _ in candidates)
    if replacement_remaining < 0:
        return packs
    if replacement_remaining > candidate_full_total * 1.05:
        return packs

    if logger:
        logger.warning(
            "fleet_api_bms: reconciling %d serial-less near-empty expansion pack(s) "
            "from aggregate remaining energy (pack sum %.0f Wh, aggregate %.0f Wh)",
            len(candidates),
            pack_remaining_total,
            total_remaining,
        )

    for pack, full, raw_remaining in candidates:
        share = replacement_remaining * (full / candidate_full_total)
        pack["rawNominalEnergyRemainingWh"] = raw_remaining
        pack["nominalEnergyRemainingWh"] = max(0.0, min(full, share))
        pack["remainingReconciledFromAggregate"] = True

    return packs
