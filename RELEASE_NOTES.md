<!-- release: v2.12.715 -->

## What's Changed

**GloBird dashboard card detects service-level sensors**
PowerSync now recognises GloBird service-level entity IDs such as `sensor.power_sync_service_920799_latest_day_cost` when deciding whether to show the GloBird Pricing card on the Home Assistant dashboard. This fixes installs where the GloBird portal sensors exist and are updating, but Home Assistant's entity-name composition removes the `globird` segment from service-level sensor IDs so the dashboard hid the card.

Update available via HACS
