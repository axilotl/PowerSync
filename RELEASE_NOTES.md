<!-- release: v2.12.704 -->

## What's Changed

**Flow Power current tariff alignment**
Flow Power tariff schedules now use the live KWatch current wholesale interval as the spot-price input for the active 30-minute PEA calculation, while still keeping that raw wholesale value out of the final retail tariff slot. This keeps `sensor.power_sync_current_import_price`, Sigenergy tariff uploads, and the PowerSync price chart aligned with Flow Power's Actual Price view after a tariff sync or Home Assistant restart.

Update available via HACS
