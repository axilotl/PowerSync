## What's Changed

**Amber: configured site ID no longer overridden on restart**
Users with multiple Amber sites who had selected a non-primary site would silently get switched back to the primary site every time Home Assistant restarted. On startup, PowerSync was fetching whichever site the Amber API considered "active" and using that regardless of what was stored in config — the configured site ID only appeared in a warning that was then ignored. The fix: if a site ID is saved in your PowerSync configuration, it's used as-is. The API is only called to discover a site during first-time setup when none has been selected yet.

**EV auto-schedule: binary sensor plug-in detection now works**
When a `binary_sensor.*` entity was configured as the generic EV charger status, the auto-schedule's plug-in check always returned "not plugged in" — binary sensors produce `on`/`off` states, but the code was looking for OCPP strings like `charging` or `preparing` which binary sensors never produce. The vehicle would be physically connected but auto-charging would never trigger. Binary sensor entities are now handled correctly: `on` means plugged in.

Update available via HACS
