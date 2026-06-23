<!-- release: v2.12.700 -->

## What's Changed

**Flow Power current price startup sync**
Flow Power installs now populate the canonical tariff schedule immediately after Home Assistant startup instead of waiting for the next scheduled sync trigger. This keeps `sensor.power_sync_current_import_price` and `sensor.power_sync_current_export_price` on the tariff-schedule price path after a restart, avoiding a temporary fallback to the raw Flow Power formula in dashboards, history, and the mobile app.

Update available via HACS
