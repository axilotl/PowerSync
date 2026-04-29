## What's Changed

**Fix: AEMO dispatch coordinator stopped polling after the first refresh (introduced in v2.12.215)**
The dispatch-trigger AEMO coordinator added in v2.12.215 was constructed but never had a listener attached to it, so Home Assistant's `DataUpdateCoordinator` ran exactly one refresh on startup (the first dispatch) and then stopped scheduling itself. HA only re-arms `_schedule_refresh` when `_listeners` is non-empty — for the existing Flow Power AEMO mode that's the price sensor, but in dispatch-trigger mode no sensor reads from the coordinator, so nothing was holding the polling loop open. The visible symptom (after the v2.12.216 thread-safety hotfix) was: exactly one "PowerSync changed Utility Rate Plan" entry appeared in the Tesla app at startup, then nothing for the next 1.5 hours despite AEMO publishing fresh dispatches every 5 minutes. The coordinator now attaches a no-op listener to keep the polling loop alive, so subsequent AEMO dispatches actually fire `SIGNAL_AEMO_NEW_DISPATCH` and trigger a tariff sync once per period.

Update available via HACS
