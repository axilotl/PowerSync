"""DataUpdateCoordinator for Powerwall local monitoring.

Runs alongside the existing ``TeslaEnergyCoordinator`` (cloud) and provides a
low-latency local snapshot every ``POWERWALL_LOCAL_POLL_INTERVAL`` seconds
when the gateway is paired. When unreachable the coordinator does not raise —
it leaves ``snapshot`` at ``None`` so consumers know to fall back to cloud data.
"""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from ..const import POWERWALL_LOCAL_POLL_INTERVAL
from .client import PowerwallLocalClient, PowerwallSnapshot
from .exceptions import PowerwallLocalError, PowerwallUnreachableError

_LOGGER = logging.getLogger(__name__)


class PowerwallLocalCoordinator(DataUpdateCoordinator[PowerwallSnapshot | None]):
    """Polls the Powerwall gateway directly for live telemetry."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: PowerwallLocalClient,
        *,
        entry_id: str,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name=f"powerwall_local_{entry_id}",
            update_interval=timedelta(seconds=POWERWALL_LOCAL_POLL_INTERVAL),
        )
        self._client = client
        self._consecutive_failures = 0
        self._last_success_ts: float | None = None

    @property
    def client(self) -> PowerwallLocalClient:
        return self._client

    @property
    def last_success_ts(self) -> float | None:
        return self._last_success_ts

    @property
    def reachable(self) -> bool:
        return self._consecutive_failures == 0

    def replace_client(self, client: PowerwallLocalClient) -> None:
        """Swap in a new client (eg after re-pair) without resetting the coordinator."""
        self._client = client
        self._consecutive_failures = 0

    async def _async_update_data(self) -> PowerwallSnapshot | None:
        try:
            snap = await self._client.get_snapshot()
        except PowerwallUnreachableError as err:
            self._consecutive_failures += 1
            if self._consecutive_failures <= 3:
                _LOGGER.debug(
                    "Powerwall local unreachable (attempt %s): %s",
                    self._consecutive_failures,
                    err,
                )
            raise UpdateFailed(f"Powerwall unreachable: {err}") from err
        except PowerwallLocalError as err:
            self._consecutive_failures += 1
            raise UpdateFailed(f"Powerwall local error: {err}") from err

        import time as _time

        self._last_success_ts = _time.time()
        self._consecutive_failures = 0
        return snap

    def snapshot_as_api(self) -> dict[str, Any]:
        """Shape the snapshot into an app-friendly dict."""
        snap = self.data
        if snap is None:
            return {
                "available": False,
                "reachable": self.reachable,
                "last_success_ts": self._last_success_ts,
            }
        return {
            "available": True,
            "reachable": True,
            "last_success_ts": self._last_success_ts,
            "soc_percent": snap.soc,
            "solar_w": snap.solar_w,
            "battery_w": snap.battery_w,
            "grid_w": snap.grid_w,
            "load_w": snap.load_w,
            "grid_status": snap.grid_status,
            "operation_mode": snap.operation_mode,
            "backup_reserve_percent": snap.backup_reserve_percent,
            "gateway_host": self._client.host,
            "gateway_din": self._client.din,
            "version": self._client.version.value,
        }
