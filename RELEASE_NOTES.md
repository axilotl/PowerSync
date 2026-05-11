<!-- release: v2.12.381 -->

## What's Changed

**Ignore invalid OCPP current ranges below the EVSE minimum**
PowerSync now treats HACS OCPP current-limit entities capped below 6A as unsupported for dynamic current control instead of writing invalid 0-5A values. Chargers with this OCPP limitation can still be started and stopped by PowerSync, while the unsupported current-limit path is skipped after detection to avoid repeated rejected profile updates.

Update available via HACS
