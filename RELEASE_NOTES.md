<!-- release: v2.12.431 -->

## What's Changed

**Use Sigenergy EVAC/EVDC plug state for charging decisions**
PowerSync now reads the configured Sigenergy charger Modbus state when deciding whether the EV is plugged in. Connected states such as `b1`, `b2`, `c1`, and `c2` can now drive scheduled and dynamic EV charging instead of being blocked by a stale `Vehicle not plugged in` decision.

**Avoid OCPP fallback masking Sigenergy chargers**
Sigenergy charger detection now runs before the OCPP and generic charger fallbacks for the Sigenergy loadpoint. This prevents mixed or migrated charger setups from returning an early OCPP `not plugged in` result when the Sigenergy charger itself is already reporting the vehicle as connected.

Update available via HACS
