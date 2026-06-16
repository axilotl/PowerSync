<!-- release: v2.12.655 -->

## What's Changed

**Fronius GEN24 BYD SOC sensors are discovered correctly**
PowerSync now recognises BYD/Fronius state-of-charge entities that use the common `state_of_charge_2` or `state_of_charge_3` suffix. This keeps the optimizer aligned with the actual battery SOC on systems where the fronius_modbus integration exposes the active BYD SOC entity with a numbered suffix, preventing plans from being based on a less specific or stale SOC sensor.

Update available via HACS
