<!-- release: v2.12.682 -->

## What's Changed

**Configurable Smart Optimization load history source**
Smart Optimization can now use a selected recorder-backed household load sensor for its historical load forecast instead of always auto-discovering `sensor.power_sync_home_load`. This helps systems that add a separate planned EV load forecast: choose a no-EV household load sensor as the historical load source so past EV charging sessions are not learned as normal house load and then counted again by the planned EV overlay.

**Safer load sensor selection**
The optimizer now rejects generated forecast/prediction sensors when they are selected as the historical load source and falls back to live load auto-discovery. Changing the load history source through settings updates the running optimizer and clears cached load history without requiring a full integration reload.

Update available via HACS
