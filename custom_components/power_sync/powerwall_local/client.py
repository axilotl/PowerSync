"""Unified local Powerwall client covering both PW2 and PW3.

PW2 exposes a plain HTTPS REST API with Bearer auth from ``/api/login/Basic``.
No RSA signing is required — just the customer password (last 5 digits of
the gateway serial) and the gateway IP.

PW3 removed most REST surface and routes config + commands through a signed
protobuf transport at ``/tedapi/v1r``. REST endpoints like
``/api/meters/aggregates`` still work with Bearer auth after the initial
customer login. The islanding command is unknown on PW3 and we try a
fallback chain: REST ``/api/v2/islanding/mode`` -> config.json rewrite ->
Storm Watch Manual Backup.

This module presents one interface to the rest of the integration so that
coordinator + service layers do not need to care which generation they're
talking to.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Any

from .exceptions import (
    PowerwallAuthError,
    PowerwallLocalError,
    PowerwallUnreachableError,
)
from .transport import TEDAPIv1rTransport

_LOGGER = logging.getLogger(__name__)

ISLAND_MODE_OFFGRID = "intentional_reconnect_failsafe"
ISLAND_MODE_ONGRID = "backup"
ISLAND_MODE_PATH = "/api/v2/islanding/mode"


class PowerwallVersion(str, Enum):
    """Known Powerwall generations. Stored in the config entry."""

    PW2 = "pw2"
    PW3 = "pw3"


@dataclass
class PowerwallSnapshot:
    """Normalized local monitoring snapshot.

    Powers are in watts (positive = flowing in the named direction). SOC is
    0-100. ``grid_status`` uses Tesla's enum strings eg ``SystemGridConnected``
    / ``SystemIslandedActive``.
    """

    soc: float | None
    solar_w: float | None
    battery_w: float | None  # positive = discharge
    grid_w: float | None  # positive = import
    load_w: float | None
    grid_status: str | None
    operation_mode: str | None
    backup_reserve_percent: int | None
    raw: dict[str, Any]


class PowerwallLocalClient:
    """Dispatches local calls between PW2 REST and PW3 TEDAPI v1r."""

    def __init__(
        self,
        host: str,
        customer_password: str,
        *,
        version: PowerwallVersion,
        private_key_pem: bytes | None = None,
        din: str | None = None,
        fleet_api_base: str | None = None,
        fleet_api_token: str | None = None,
        energy_site_id: int | str | None = None,
    ) -> None:
        self._host = host
        self._customer_password = customer_password
        self._version = version
        self._din = din
        self._fleet_api_base = fleet_api_base
        self._fleet_api_token = fleet_api_token
        self._energy_site_id = energy_site_id

        # Saved pre-curtailment state so we can restore the user's actual
        # operation mode + backup reserve when curtailment ends.
        self._saved_real_mode: str | None = None
        self._saved_reserve_percent: int | None = None
        self._curtailment_active = False

        # Both generations use the same signed transport for symmetry — on
        # PW2 the RSA signing path is unused but the REST helpers live in
        # the same class so we avoid duplicating the session/SSL setup.
        if private_key_pem is None:
            # Unsigned client (PW2-only, or pre-pairing monitoring).
            self._transport: TEDAPIv1rTransport | None = None
            self._unsigned = _UnsignedRESTClient(host, customer_password)
        else:
            self._transport = TEDAPIv1rTransport(
                host, private_key_pem, customer_password
            )
            self._unsigned = None

    @property
    def version(self) -> PowerwallVersion:
        return self._version

    @property
    def host(self) -> str:
        return self._host

    @property
    def din(self) -> str | None:
        if self._din:
            return self._din
        if self._transport and self._transport.din:
            return self._transport.din
        return None

    async def _get(self, path: str) -> Any | None:
        if self._transport is not None:
            return await self._transport.api_get(path)
        assert self._unsigned is not None
        return await self._unsigned.api_get(path)

    async def _post(self, path: str, body: dict[str, Any]) -> Any | None:
        if self._transport is not None:
            return await self._transport.api_post(path, body)
        assert self._unsigned is not None
        return await self._unsigned.api_post(path, body)

    async def login(self) -> bool:
        if self._transport is not None:
            ok = await self._transport.login()
            if ok:
                # Always refresh the DIN from the gateway — the stored
                # value might be a partial serial instead of the full
                # {part_number}--{serial_number} the TEDAPI v1r transport
                # needs for TLV signature personalization.
                fetched = await self._transport.fetch_din()
                if fetched:
                    self._din = fetched
            return ok
        assert self._unsigned is not None
        return await self._unsigned.login()

    async def get_snapshot(self) -> PowerwallSnapshot:
        """Fetch the standard monitoring set in parallel-friendly order."""
        meters = await self._get("/api/meters/aggregates") or {}
        soe = await self._get("/api/system_status/soe") or {}
        grid = await self._get("/api/system_status/grid_status") or {}
        operation = await self._get("/api/operation") or {}

        def _watts(section: dict[str, Any] | None) -> float | None:
            if not isinstance(section, dict):
                return None
            v = section.get("instant_power")
            return float(v) if v is not None else None

        return PowerwallSnapshot(
            soc=_float_or_none(soe.get("percentage")),
            solar_w=_watts(meters.get("solar")),
            battery_w=_watts(meters.get("battery")),
            grid_w=_watts(meters.get("site")),
            load_w=_watts(meters.get("load")),
            grid_status=grid.get("grid_status") if isinstance(grid, dict) else None,
            operation_mode=(
                operation.get("real_mode") if isinstance(operation, dict) else None
            ),
            backup_reserve_percent=_int_or_none(
                operation.get("backup_reserve_percent")
                if isinstance(operation, dict)
                else None
            ),
            raw={
                "meters": meters,
                "soe": soe,
                "grid": grid,
                "operation": operation,
            },
        )

    async def go_off_grid(self) -> bool:
        """Physically disconnect from the grid (contactor open).

        Uses Tesla cloud ``device_command`` with the captured protobuf.
        Causes an inverter restart (~30s solar dropout) — use only for
        manual/deliberate islanding, NOT for automated curtailment.
        """
        if self._version == PowerwallVersion.PW3 and self._din:
            _LOGGER.info("go_off_grid: sending device_command via cloud proxy")
            return await self._send_device_command(off_grid=True)

        body = {"island_mode": ISLAND_MODE_OFFGRID}
        result = await self._post(ISLAND_MODE_PATH, body)
        if result is not None:
            _LOGGER.info("go_off_grid: REST islanding accepted on %s", self._host)
            return True

        _LOGGER.warning("go_off_grid: all paths failed on %s", self._host)
        return False

    async def reconnect_grid(self) -> bool:
        """Reconnect to the grid (contactor close).

        Uses Tesla cloud ``device_command`` with the captured protobuf.
        """
        if self._version == PowerwallVersion.PW3 and self._din:
            _LOGGER.info("reconnect_grid: sending device_command via cloud proxy")
            return await self._send_device_command(off_grid=False)

        body = {"island_mode": ISLAND_MODE_ONGRID}
        result = await self._post(ISLAND_MODE_PATH, body)
        if result is not None:
            return True
        return False

    async def curtail_via_backup_mode(self) -> bool:
        """Stop grid export by switching to backup mode + 100% reserve.

        Uses local TEDAPI config.json write — no contactor cycling, no
        inverter restart, no solar dropout. Takes ~90s for the gateway
        to apply the config change. Saves the user's current operation
        mode + reserve so ``restore_from_curtailment`` can put them back.

        This is the mechanism for automated curtailment (negative pricing,
        demand charge windows). For manual off-grid use ``go_off_grid``.
        """
        if not self._transport or not self._din:
            _LOGGER.warning("curtail_via_backup_mode: no transport/din")
            return False

        # Read current config to save the user's values
        try:
            config = await self._transport.read_config(self._din)
            if config:
                self._saved_real_mode = config.get("default_real_mode", "self_consumption")
                si = config.get("site_info", {})
                self._saved_reserve_percent = int(si.get("backup_reserve_percent", 5))
                _LOGGER.info(
                    "curtail: saved mode=%s reserve=%s%%",
                    self._saved_real_mode, self._saved_reserve_percent,
                )
        except Exception as err:
            _LOGGER.warning("curtail: failed to read pre-curtailment config: %s", err)
            if self._saved_real_mode is None:
                self._saved_real_mode = "self_consumption"
            if self._saved_reserve_percent is None:
                self._saved_reserve_percent = 5

        ok = await self._transport.write_config(self._din, {
            "default_real_mode": "backup",
            "site_info.backup_reserve_percent": 100,
        })
        if ok:
            self._curtailment_active = True
            _LOGGER.info("curtail: config write succeeded — backup/100%%")
        else:
            _LOGGER.warning("curtail: config write failed")
        return ok

    async def restore_from_curtailment(self) -> bool:
        """Restore the user's operation mode + reserve after curtailment.

        Writes back the values captured by ``curtail_via_backup_mode``.
        """
        if not self._transport or not self._din:
            return False

        mode = self._saved_real_mode or "self_consumption"
        reserve = self._saved_reserve_percent if self._saved_reserve_percent is not None else 5

        _LOGGER.info("restore: writing mode=%s reserve=%s%%", mode, reserve)
        ok = await self._transport.write_config(self._din, {
            "default_real_mode": mode,
            "site_info.backup_reserve_percent": reserve,
        })
        if ok:
            self._curtailment_active = False
            _LOGGER.info("restore: config write succeeded")
        else:
            _LOGGER.warning("restore: config write failed")
        return ok

    @property
    def curtailment_active(self) -> bool:
        return self._curtailment_active

    # Off-grid: base64 protobuf — captured from Tesla app via mitmproxy.
    # Decodes to field 6 → field 5 → field 1 = 2 (setIslandMode mode=2).
    _OFFGRID_MSG = "MgQqAggC"
    # Reconnect: base64 protobuf — captured from Tesla app via mitmproxy.
    # Different message structure than off-grid (field 1 → field 22 empty).
    _ONGRID_MSG = "CgOyAQA="

    async def _send_device_command(self, *, off_grid: bool) -> bool:
        """Send off-grid/reconnect via Tesla cloud ``/device_command`` endpoint.

        This is the exact mechanism the Tesla mobile app uses — discovered
        via mitmproxy capture of the app's "Go Off-Grid" button. The cloud
        relays a base64-encoded protobuf to the gateway which physically
        opens or closes the grid contactor. Confirmed working on PW3
        firmware 26.2.1.
        """
        if not self._fleet_api_base or not self._fleet_api_token or not self._energy_site_id:
            _LOGGER.warning(
                "device_command: missing fleet_api_base=%s token=%s site=%s",
                bool(self._fleet_api_base),
                bool(self._fleet_api_token),
                self._energy_site_id,
            )
            return False

        import aiohttp

        msg = self._OFFGRID_MSG if off_grid else self._ONGRID_MSG
        action = "off_grid" if off_grid else "on_grid"
        url = (
            f"{self._fleet_api_base}/api/1/energy_sites/"
            f"{self._energy_site_id}/device_command"
        )
        payload = {
            "data": {
                "target_id": self._din,
                "energy_device_message": msg,
                "command_timeout_s": 10,
                "identifier_type": 1,
            }
        }
        headers = {
            "Authorization": f"Bearer {self._fleet_api_token}",
            "Content-Type": "application/json",
        }
        _LOGGER.info(
            "device_command: %s → %s (din=%s)", action, url, self._din
        )
        try:
            async with aiohttp.ClientSession() as sess:
                async with sess.post(
                    url, json=payload, headers=headers, timeout=aiohttp.ClientTimeout(total=15)
                ) as resp:
                    if resp.status != 200:
                        body = await resp.text()
                        _LOGGER.warning(
                            "device_command %s failed (%s): %s",
                            action, resp.status, body[:300],
                        )
                        return False
                    data = await resp.json()
                    _LOGGER.info("device_command %s: response=%s", action, str(data)[:300])
                    return "response" in data
        except Exception as err:
            _LOGGER.error("device_command %s error: %s", action, err)
            return False

    async def verify_paired(self) -> bool:
        """Best-effort check that the RSA key is still accepted.

        Sends a trivial TEDAPI read; if the gateway replies with
        MESSAGEFAULT_ERROR_UNKNOWN_KEY_ID the transport raises
        ``PowerwallSignatureError`` which we surface as "not paired".
        """
        if self._transport is None:
            return await self.login()
        if not self._din:
            self._din = await self._transport.fetch_din()
        if not self._din:
            return False
        try:
            config = await self._transport.read_config(self._din)
        except PowerwallLocalError:
            return False
        return config is not None


def _float_or_none(value: Any) -> float | None:
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _int_or_none(value: Any) -> int | None:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


class _UnsignedRESTClient:
    """Minimal REST client for PW2 without an RSA transport.

    Shares the self-signed SSL context with the v1r transport but skips all
    protobuf machinery. Used before pairing completes so the app can still
    display live data, and on pure PW2 installs where pairing is optional.
    """

    def __init__(self, host: str, customer_password: str) -> None:
        import aiohttp

        from .transport import _insecure_ssl_context

        self._host = host
        self._customer_password = customer_password
        self._ssl = _insecure_ssl_context()
        self._timeout = aiohttp.ClientTimeout(total=8.0)
        self._token: str | None = None
        self._aiohttp = aiohttp

    async def _session(self):
        connector = self._aiohttp.TCPConnector(ssl=self._ssl, limit=4)
        return self._aiohttp.ClientSession(
            connector=connector, timeout=self._timeout
        )

    async def login(self) -> bool:
        url = f"https://{self._host}/api/login/Basic"
        payload = {
            "username": "customer",
            "password": self._customer_password,
            "email": "customer@customer.domain",
            "clientInfo": {"timezone": "UTC"},
        }
        try:
            async with await self._session() as sess:
                async with sess.post(url, json=payload) as resp:
                    if resp.status in (401, 403):
                        raise PowerwallAuthError(
                            f"Gateway rejected customer password ({resp.status})"
                        )
                    if resp.status != 200:
                        return False
                    data = await resp.json()
                    self._token = data.get("token")
                    return self._token is not None
        except self._aiohttp.ClientError as err:
            raise PowerwallUnreachableError(str(err)) from err

    async def api_get(self, path: str) -> Any | None:
        if not self._token and not await self.login():
            return None
        url = f"https://{self._host}{path}"
        headers = {"Authorization": f"Bearer {self._token}"}
        try:
            async with await self._session() as sess:
                async with sess.get(url, headers=headers) as resp:
                    if resp.status in (401, 403) and await self.login():
                        headers["Authorization"] = f"Bearer {self._token}"
                        async with sess.get(url, headers=headers) as r2:
                            if r2.status != 200:
                                return None
                            return await r2.json()
                    if resp.status != 200:
                        return None
                    return await resp.json()
        except self._aiohttp.ClientError as err:
            raise PowerwallUnreachableError(str(err)) from err

    async def api_post(self, path: str, body: dict[str, Any]) -> Any | None:
        if not self._token and not await self.login():
            return None
        url = f"https://{self._host}{path}"
        headers = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/json",
        }
        try:
            async with await self._session() as sess:
                async with sess.post(url, json=body, headers=headers) as resp:
                    if resp.status in (401, 403) and await self.login():
                        headers["Authorization"] = f"Bearer {self._token}"
                        async with sess.post(url, json=body, headers=headers) as r2:
                            if r2.status not in (200, 201, 204):
                                return None
                            return {} if r2.status == 204 else await r2.json()
                    if resp.status not in (200, 201, 204):
                        return None
                    return {} if resp.status == 204 else await resp.json()
        except self._aiohttp.ClientError as err:
            raise PowerwallUnreachableError(str(err)) from err
