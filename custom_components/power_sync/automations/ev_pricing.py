"""Shared EV charging price lookup helpers."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any

try:
    from homeassistant.util import dt as dt_util
except ModuleNotFoundError:  # pragma: no cover - lightweight unit-test fallback
    class _DtUtil:
        @staticmethod
        def now() -> datetime:
            return datetime.now(timezone.utc)

    dt_util = _DtUtil()

from ..const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def _prices_from_current(data: dict[str, Any] | None) -> tuple[float, float] | None:
    """Extract import/export prices from Amber-shaped current price data."""
    if not data:
        return None

    current_prices = data.get("current", [])
    if not current_prices:
        return None

    import_price = None
    export_price = None
    for price in current_prices:
        if price.get("channelType") == "general":
            import_price = price.get("perKwh")
        elif price.get("channelType") == "feedIn":
            feed_in = price.get("perKwh")
            if feed_in is not None:
                export_price = abs(feed_in)

    if import_price is None:
        return None

    return (
        import_price,
        export_price if export_price is not None else 8.0,
    )


def get_current_ev_prices(hass: Any, entry_id: str) -> tuple[float, float]:
    """Get current import/export prices for EV charging session accounting.

    Returns prices in cents/kWh.
    """
    import_price = 30.0
    export_price = 8.0

    entry_data = hass.data.get(DOMAIN, {}).get(entry_id, {})

    # Dynamic provider coordinators expose Amber-shaped c/kWh current data.
    for coordinator_key in (
        "amber_coordinator",
        "localvolts_coordinator",
        "octopus_coordinator",
        "epex_coordinator",
        "aemo_sensor_coordinator",
    ):
        coordinator = entry_data.get(coordinator_key)
        prices = _prices_from_current(getattr(coordinator, "data", None))
        if prices is not None:
            return prices

    # Globird/AEMO VPP and other static TOU providers store a tariff schedule.
    # Resolve the live period, otherwise a free/cheap window can be costed with
    # an old cached or default price.
    tariff_schedule = entry_data.get("tariff_schedule")
    if tariff_schedule:
        try:
            from .. import get_current_price_from_tariff_schedule

            import_price, export_price, _current_period = (
                get_current_price_from_tariff_schedule(tariff_schedule)
            )
            return import_price, export_price
        except Exception as err:
            _LOGGER.debug("Could not resolve EV tariff schedule price: %s", err)
            import_price = tariff_schedule.get("buy_price", 30.0)
            export_price = tariff_schedule.get("sell_price", 8.0)
            return import_price, export_price

    # Sigenergy tariff slots are already in c/kWh.
    sigenergy_tariff = entry_data.get("sigenergy_tariff")
    if sigenergy_tariff:
        buy_prices = sigenergy_tariff.get("buy_prices", [])
        sell_prices = sigenergy_tariff.get("sell_prices", [])
        now = dt_util.now()
        current_time = f"{now.hour:02d}:{30 if now.minute >= 30 else 0:02d}"
        if buy_prices:
            for slot in buy_prices:
                if slot.get("timeRange", "").startswith(current_time):
                    import_price = slot.get("price", 30.0)
                    break
        if sell_prices:
            for slot in sell_prices:
                if slot.get("timeRange", "").startswith(current_time):
                    export_price = slot.get("price", 8.0)
                    break
        return import_price, export_price

    price_data = entry_data.get("current_prices", {})
    if price_data:
        import_price = price_data.get("import_cents", 30.0)
        export_price = price_data.get("export_cents", 8.0)

    return import_price, export_price
