"""Solax inverter controller via homeassistant-solax-modbus integration.

Controls Solax inverters using the wills106/homeassistant-solax-modbus
integration's entities (number.solax_export_control_user_limit).

Supports load-following curtailment and zero-export via export power limiting.

Reference: https://github.com/wills106/homeassistant-solax-modbus
"""
import logging
from typing import Optional

from .base import InverterController, InverterState, InverterStatus

_LOGGER = logging.getLogger(__name__)

# Default entity IDs from solax-modbus integration
DEFAULT_EXPORT_LIMIT_ENTITY = "number.solax_export_control_user_limit"
DEFAULT_FACTORY_LIMIT_ENTITY = "sensor.solax_export_control_factory_limit"


class SolaxController(InverterController):
    """Controller for Solax inverters via HA entity service calls.

    Uses the homeassistant-solax-modbus integration's entities to control
    the inverter's export power limit. Requires the integration to be
    installed and configured separately.

    Supports load-following curtailment via export_control_user_limit.
    """

    def __init__(
        self,
        host: str,
        port: int = 502,
        slave_id: int = 1,
        model: Optional[str] = None,
        hass=None,
        export_limit_entity: Optional[str] = None,
        factory_limit_entity: Optional[str] = None,
    ):
        """Initialize Solax controller.

        Args:
            host: Not used (Solax uses HA entities, not direct connection)
            port: Not used
            slave_id: Not used
            model: Solax model (informational)
            hass: HomeAssistant instance (required for service calls)
            export_limit_entity: Entity ID for export limit control
            factory_limit_entity: Entity ID for factory limit sensor
        """
        super().__init__(host, port, slave_id, model)
        self._hass = hass
        self._export_limit_entity = export_limit_entity or DEFAULT_EXPORT_LIMIT_ENTITY
        self._factory_limit_entity = factory_limit_entity or DEFAULT_FACTORY_LIMIT_ENTITY
        self._original_limit: float | None = None

    async def connect(self) -> bool:
        """Check that the Solax integration entities exist."""
        if not self._hass:
            _LOGGER.error("Solax controller requires hass instance")
            return False

        state = self._hass.states.get(self._export_limit_entity)
        if not state:
            _LOGGER.error(
                "Solax export limit entity not found: %s. "
                "Is the homeassistant-solax-modbus integration installed?",
                self._export_limit_entity,
            )
            return False

        self._connected = True
        _LOGGER.info("Solax controller connected via HA entity: %s", self._export_limit_entity)
        return True

    async def disconnect(self) -> None:
        """No-op — entity-based controller has no connection to close."""
        pass

    async def get_status(self) -> InverterState:
        """Get current inverter state."""
        if not self._hass:
            return InverterState(
                status=InverterStatus.ERROR,
                is_curtailed=False,
                error_message="No hass instance",
            )

        state = self._hass.states.get(self._export_limit_entity)
        if not state or state.state in ("unavailable", "unknown"):
            return InverterState(
                status=InverterStatus.OFFLINE,
                is_curtailed=False,
            )

        try:
            current_limit = float(state.state)
        except (ValueError, TypeError):
            current_limit = None

        # Read factory limit to determine if curtailed
        factory_state = self._hass.states.get(self._factory_limit_entity)
        factory_limit = None
        if factory_state and factory_state.state not in ("unavailable", "unknown"):
            try:
                factory_limit = float(factory_state.state)
            except (ValueError, TypeError):
                pass

        is_curtailed = (
            current_limit is not None
            and factory_limit is not None
            and current_limit < factory_limit
        )

        return InverterState(
            status=InverterStatus.CURTAILED if is_curtailed else InverterStatus.ONLINE,
            is_curtailed=is_curtailed,
            power_output_w=current_limit,
            attributes={
                "export_limit_w": current_limit,
                "factory_limit_w": factory_limit,
            },
        )

    async def curtail(
        self,
        home_load_w: float | None = None,
        rated_capacity_w: float | None = None,
    ) -> bool:
        """Curtail inverter export by setting export limit.

        Args:
            home_load_w: Home load in watts for load-following mode.
                        If None, sets zero export.
            rated_capacity_w: Not used (limit is absolute watts, not percentage)

        Returns:
            True if successful
        """
        if not self._hass:
            return False

        # Save current limit for restore (if not already saved)
        if self._original_limit is None:
            factory_state = self._hass.states.get(self._factory_limit_entity)
            if factory_state and factory_state.state not in ("unavailable", "unknown"):
                try:
                    self._original_limit = float(factory_state.state)
                except (ValueError, TypeError):
                    pass
            if self._original_limit is None:
                # Fallback: read current setting
                state = self._hass.states.get(self._export_limit_entity)
                if state and state.state not in ("unavailable", "unknown"):
                    try:
                        self._original_limit = float(state.state)
                    except (ValueError, TypeError):
                        self._original_limit = 5000  # Safe fallback

        # Calculate target export limit
        if home_load_w is not None and home_load_w > 0:
            # Load-following: allow export up to home load
            target_w = max(0, int(home_load_w))
        else:
            # Zero export
            target_w = 0

        try:
            await self._hass.services.async_call(
                "number",
                "set_value",
                {"entity_id": self._export_limit_entity, "value": target_w},
                blocking=True,
            )
            _LOGGER.info(
                "Solax export limit set to %dW (was %sW)",
                target_w,
                int(self._original_limit) if self._original_limit else "unknown",
            )
            return True
        except Exception as e:
            _LOGGER.error("Failed to set Solax export limit: %s", e)
            return False

    async def restore(self) -> bool:
        """Restore inverter to normal operation (factory export limit)."""
        if not self._hass:
            return False

        # Determine restore value
        restore_w = self._original_limit

        if restore_w is None:
            # Try reading factory limit
            factory_state = self._hass.states.get(self._factory_limit_entity)
            if factory_state and factory_state.state not in ("unavailable", "unknown"):
                try:
                    restore_w = float(factory_state.state)
                except (ValueError, TypeError):
                    pass

        if restore_w is None:
            _LOGGER.warning("No factory limit available — setting export limit to 5000W as fallback")
            restore_w = 5000

        try:
            await self._hass.services.async_call(
                "number",
                "set_value",
                {"entity_id": self._export_limit_entity, "value": int(restore_w)},
                blocking=True,
            )
            _LOGGER.info("Solax export limit restored to %dW", int(restore_w))
            self._original_limit = None
            return True
        except Exception as e:
            _LOGGER.error("Failed to restore Solax export limit: %s", e)
            return False
