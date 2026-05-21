"""SolarEdge inverter controller for active-power curtailment.

Uses SolarEdge Modbus TCP/SunSpec for telemetry and the SolarEdge power
control register 0xF001 for active power limiting. If direct Modbus is not
available, falls back to known Home Assistant SolarEdge Modbus number entities.
"""

from __future__ import annotations

import asyncio
import logging
import math
from typing import Optional

from .base import InverterController, InverterState, InverterStatus

_LOGGER = logging.getLogger(__name__)


class SolarEdgeController(InverterController):
    """Controller for SolarEdge inverters via Modbus TCP or HA entities."""

    REG_INVERTER_DATA = 40071
    REG_ACTIVE_POWER_LIMIT = 0xF001
    TIMEOUT_SECONDS = 10.0
    DEFAULT_RATED_POWER_W = 5000

    STATUS_TEXT = {
        1: "off",
        2: "sleeping",
        3: "starting",
        4: "mppt",
        5: "throttled",
        6: "shutting_down",
        7: "fault",
        8: "standby",
    }

    def __init__(
        self,
        host: str,
        port: int = 502,
        slave_id: int = 1,
        model: Optional[str] = None,
        rated_power_w: Optional[float] = None,
        entity_prefix: Optional[str] = None,
        hass=None,
    ) -> None:
        super().__init__(host, port, slave_id, model)
        self.rated_power_w = float(rated_power_w or self.DEFAULT_RATED_POWER_W)
        self.entity_prefix = (entity_prefix or "").strip()
        self._hass = hass
        self._client = None
        self._lock = asyncio.Lock()
        self._slave_in_client = False
        self._slave_param = "device_id"
        self._use_entity_mode = False
        self._active_power_limit_entity: str | None = None

    async def connect(self) -> bool:
        """Connect to SolarEdge via direct Modbus, falling back to HA entities."""
        async with self._lock:
            if self._client and getattr(self._client, "connected", False):
                self._connected = True
                self._use_entity_mode = False
                return True

            if self.host and self.host not in ("0.0.0.0", "none"):
                try:
                    from pymodbus.client import AsyncModbusTcpClient

                    self._slave_in_client = False
                    try:
                        self._client = AsyncModbusTcpClient(
                            host=self.host,
                            port=self.port,
                            timeout=self.TIMEOUT_SECONDS,
                            device_id=self.slave_id,
                        )
                        self._slave_in_client = True
                    except TypeError:
                        try:
                            self._client = AsyncModbusTcpClient(
                                host=self.host,
                                port=self.port,
                                timeout=self.TIMEOUT_SECONDS,
                                slave=self.slave_id,
                            )
                            self._slave_in_client = True
                        except TypeError:
                            self._client = AsyncModbusTcpClient(
                                host=self.host,
                                port=self.port,
                                timeout=self.TIMEOUT_SECONDS,
                            )

                    if await self._client.connect():
                        self._connected = True
                        self._use_entity_mode = False
                        _LOGGER.info(
                            "Connected to SolarEdge inverter at %s:%s (slave %s)",
                            self.host,
                            self.port,
                            self.slave_id,
                        )
                        return True
                except Exception as err:
                    _LOGGER.warning(
                        "SolarEdge Modbus connection failed for %s:%s: %s",
                        self.host,
                        self.port,
                        err,
                    )

            entity = self._find_active_power_limit_entity()
            if entity:
                self._active_power_limit_entity = entity
                self._connected = True
                self._use_entity_mode = True
                _LOGGER.info("SolarEdge using HA entity fallback: %s", entity)
                return True

            self._connected = False
            return False

    async def disconnect(self) -> None:
        """Close the direct Modbus connection."""
        async with self._lock:
            if self._client:
                self._client.close()
                self._client = None
            self._connected = False

    async def curtail(
        self,
        home_load_w: Optional[float] = None,
        rated_capacity_w: Optional[float] = None,
    ) -> bool:
        """Apply SolarEdge active power limiting.

        ``home_load_w`` maps to a percentage of rated inverter power. ``None``
        or non-positive load means full curtailment (0% active power limit).
        """
        rated_w = float(rated_capacity_w or self.rated_power_w or self.DEFAULT_RATED_POWER_W)
        if home_load_w is not None and home_load_w > 0 and rated_w > 0:
            target_pct = math.ceil((float(home_load_w) / rated_w) * 100.0)
        else:
            target_pct = 0
        target_pct = max(0, min(100, int(target_pct)))

        ok = await self._set_active_power_limit(target_pct)
        if ok:
            _LOGGER.info(
                "SolarEdge active power limit set to %d%% (home_load=%sW, rated=%sW)",
                target_pct,
                int(home_load_w) if home_load_w is not None else "none",
                int(rated_w),
            )
        return ok

    async def restore(self) -> bool:
        """Restore SolarEdge active power limit to 100%."""
        ok = await self._set_active_power_limit(100)
        if ok:
            _LOGGER.info("SolarEdge active power limit restored to 100%%")
        return ok

    async def get_status(self) -> InverterState:
        """Read current SolarEdge telemetry and curtailment state."""
        if not self._connected and not await self.connect():
            return InverterState(
                status=InverterStatus.OFFLINE,
                is_curtailed=False,
                error_message="SolarEdge connection unavailable",
            )

        attrs: dict[str, object] = {
            "mode": "entity" if self._use_entity_mode else "modbus",
            "rated_ac_power_w": self.rated_power_w,
        }

        limit_pct = await self._get_active_power_limit()
        if limit_pct is not None:
            attrs["active_power_limit_percent"] = limit_pct

        if self._use_entity_mode:
            is_curtailed = limit_pct is not None and limit_pct < 100
            return InverterState(
                status=InverterStatus.CURTAILED if is_curtailed else InverterStatus.ONLINE,
                is_curtailed=is_curtailed,
                power_limit_percent=limit_pct,
                attributes=attrs,
            )

        telemetry = await self._read_inverter_telemetry()
        attrs.update(telemetry)
        status_code = telemetry.get("status_code")
        status_text = telemetry.get("status")
        is_curtailed = bool(
            (limit_pct is not None and limit_pct < 100)
            or status_code == 5
            or status_text == "throttled"
        )

        return InverterState(
            status=InverterStatus.CURTAILED if is_curtailed else InverterStatus.ONLINE,
            is_curtailed=is_curtailed,
            power_output_w=telemetry.get("ac_power_w"),
            power_limit_percent=limit_pct,
            attributes=attrs,
        )

    async def _set_active_power_limit(self, percent: int) -> bool:
        if not self._connected and not await self.connect():
            _LOGGER.error("SolarEdge active power limit write failed: not connected")
            return False

        if self._use_entity_mode:
            entity = self._active_power_limit_entity or self._find_active_power_limit_entity()
            if not entity or not self._hass:
                return False
            try:
                await self._hass.services.async_call(
                    "number",
                    "set_value",
                    {"entity_id": entity, "value": percent},
                    blocking=True,
                )
                return True
            except Exception as err:
                _LOGGER.error("SolarEdge entity write failed for %s: %s", entity, err)
                return False

        if not self._client or not self._client.connected:
            return False
        try:
            if self._slave_in_client:
                result = await self._client.write_register(
                    address=self.REG_ACTIVE_POWER_LIMIT,
                    value=int(percent),
                )
            else:
                result = await self._try_modbus_call(
                    self._client.write_register,
                    address=self.REG_ACTIVE_POWER_LIMIT,
                    value=int(percent),
                )
            if result is None or result.isError():
                _LOGGER.error("SolarEdge active power limit write rejected: %s", result)
                return False
            return True
        except Exception as err:
            _LOGGER.error("SolarEdge active power limit write error: %s", err)
            return False

    async def _get_active_power_limit(self) -> int | None:
        if self._use_entity_mode:
            entity = self._active_power_limit_entity or self._find_active_power_limit_entity()
            state = self._hass.states.get(entity) if self._hass and entity else None
            if state and state.state not in ("unknown", "unavailable", None):
                try:
                    return int(float(state.state))
                except (TypeError, ValueError):
                    return None
            return None

        regs = await self._read_holding_registers(self.REG_ACTIVE_POWER_LIMIT, 1)
        if not regs:
            return None
        return int(regs[0])

    async def _read_inverter_telemetry(self) -> dict[str, object]:
        regs = await self._read_holding_registers(self.REG_INVERTER_DATA, 38)
        if not regs:
            return {}

        def scaled(value: int, sf: int) -> float:
            return round(value * (10 ** sf), max(0, -sf))

        ac_power = scaled(self._to_signed16(regs[12]), self._to_signed16(regs[13]))
        dc_power = scaled(self._to_signed16(regs[29]), self._to_signed16(regs[30]))
        status_code = self._to_signed16(regs[36])

        return {
            "ac_power_w": ac_power,
            "dc_power_w": dc_power,
            "status_code": status_code,
            "status": self.STATUS_TEXT.get(status_code, f"unknown_{status_code}"),
        }

    async def _read_holding_registers(self, address: int, count: int) -> list[int] | None:
        if not self._client or not self._client.connected:
            if not await self.connect():
                return None
        try:
            if self._slave_in_client:
                result = await self._client.read_holding_registers(
                    address=address,
                    count=count,
                )
            else:
                result = await self._try_modbus_call(
                    self._client.read_holding_registers,
                    address=address,
                    count=count,
                )
            if result is None or result.isError():
                _LOGGER.debug("SolarEdge Modbus read failed at 0x%04X: %s", address, result)
                return None
            return list(result.registers)
        except Exception as err:
            _LOGGER.debug("SolarEdge Modbus read error at 0x%04X: %s", address, err)
            return None

    async def _try_modbus_call(self, method, **kwargs):
        for param in ("device_id", "slave", "unit"):
            try:
                return await method(**kwargs, **{param: self.slave_id})
            except TypeError:
                continue
        try:
            return await method(**kwargs)
        except TypeError:
            _LOGGER.error("Could not find compatible pymodbus API for %s", method.__name__)
            return None

    def _find_active_power_limit_entity(self) -> str | None:
        if not self._hass:
            return None

        prefixes = []
        if self.entity_prefix:
            prefixes.append(self.entity_prefix)
        prefixes.extend(["solaredge", "solaredge_i1"])

        candidates: list[str] = []
        for prefix in prefixes:
            candidates.extend(
                [
                    f"number.{prefix}_active_power_limit",
                    f"number.{prefix}_nominal_active_power_limit",
                    f"number.{prefix}_i1_active_power_limit",
                    f"number.{prefix}_i1_nominal_active_power_limit",
                ]
            )

        for entity_id in dict.fromkeys(candidates):
            state = self._hass.states.get(entity_id)
            if state is not None:
                return entity_id
        return None

    @staticmethod
    def _to_signed16(value: int) -> int:
        return value - 0x10000 if value >= 0x8000 else value
