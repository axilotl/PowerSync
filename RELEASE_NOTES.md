## What's Changed

**Tesla Energy Site capability probe**
On first connection PowerSync now probes the Tesla Fleet API to detect which energy-site features your specific Powerwall installation actually supports — Storm Watch, off-grid EV reserve, and VPP/grid-services programs. Unsupported features (e.g. VPP programs outside the US) simply don't appear in HA or the mobile app, so you only ever see controls that actually work for your site.

**Storm Watch control**
A new switch entity (`switch.power_sync_tesla_storm_watch`) lets you enable or disable Tesla's predictive pre-charging before severe weather, alongside a `binary_sensor.power_sync_tesla_storm_watch_active` that tells you when Tesla is currently treating an event as imminent. Both are also surfaced in the mobile app's Controls screen and as a new automation action and weather trigger condition.

**Off-grid EV charging reserve**
You can now set a separate battery reserve percentage that Tesla holds back specifically for vehicle charging during a grid outage, via a new `number.power_sync_tesla_off_grid_ev_reserve` entity, the mobile app Controls screen, and the new `set_off_grid_ev_reserve` service and automation action. This is independent of the regular backup reserve.

**Tesla VPP / grid-services enrollment**
For sites that are eligible (typically US Tesla Electric / VPP customers), PowerSync fetches the list of available programs from Tesla and creates one switch per program (e.g. `switch.power_sync_tesla_vpp_tesla_electric`). You can now enroll or unenroll directly from HA, the mobile Controls screen, or via automation — no more needing the Tesla app to manage VPP participation.

**Powerwall settings now first-class HA entities**
Backup reserve, operation mode (TOU vs Self-Consumption), grid export rule, and grid charging — previously only callable via services — are now real HA entities (`number`, `select`, and `switch`) on the PowerSync device. You can use them in any HA dashboard or automation without writing service calls. A `binary_sensor.power_sync_tesla_manual_export_override` also surfaces whether you've manually overridden the optimiser's export control.

**Unified Tesla API client with Retry-After handling**
New service handlers, mobile API endpoints, and automation actions all flow through a single `_tesla_api_call` helper on the coordinator that handles retries, exponential backoff, and Retry-After headers consistently. This replaces several copies of inline retry logic and makes future Tesla API additions much cleaner.

**New mobile API endpoints**
Three new HTTP endpoints — `/api/power_sync/tesla/storm_watch`, `/api/power_sync/tesla/off_grid_ev_reserve`, and `/api/power_sync/tesla/vpp_programs` — back the new mobile Controls screen widgets. The existing `/api/power_sync/powerwall_settings` response is also extended with a `capabilities` block, current Storm Watch state, current off-grid EV reserve, and the site's country code so the app knows which controls to render.

Update available via HACS
