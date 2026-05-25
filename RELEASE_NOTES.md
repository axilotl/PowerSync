<!-- release: v2.12.467 -->

## What's Changed

**FoxESS entity bridge auto-discovery**
PowerSync's FoxESS entity bridge now recognizes unprefixed entity IDs created by foxess_modbus, such as `sensor.battery_soc_1`, `select.work_mode`, `number.force_charge_power`, and `number.min_soc_on_grid`. This fixes setup failing with `foxess_entity_missing_entities` when the selected FoxESS Modbus integration is valid but does not use a `foxess_` entity prefix.

**Regression coverage**
Added focused entity-bridge coverage for the unprefixed FoxESS Modbus surface reported in issue #90, confirming telemetry, work mode, force-charge power, and reserve controls are discovered correctly.

Update available via HACS
