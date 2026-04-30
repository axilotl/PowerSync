## What's Changed

**Fix the local coordinator falling silent after one fetch (root cause of stuck-sensor reports)**
The local Powerwall coordinator was running its forced first refresh on startup, then permanently going silent. Symptoms: mobile app and HA tiles freeze on whatever value was in the gateway snapshot at startup time. Cause: HA's `DataUpdateCoordinator` pauses its periodic schedule when its listener count drops to zero — an optimisation that's normally fine because entity listeners attach in `async_added_to_hass`. But sensor setup and `ensure_coordinator` race, and when sensors win the race they look up the local coordinator before it exists, find None, and never subscribe. The coordinator does its one-shot first refresh, sees zero listeners, and goes to sleep forever. This bug was always latent — pre-2.12.224 nothing read from the local coord at all, so no one noticed. The 30s freshness guard from 2.12.227 protects against the *symptom*; this release fixes the underlying *cause*.

Fix: the coordinator now anchors a keep-alive no-op listener inside its own `__init__`, so the periodic schedule stays armed regardless of how downstream consumers (sensors, mobile app HTTP view) subscribe.

Update available via HACS
