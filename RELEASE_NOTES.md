## What's Changed

Three Tesla integration bug fixes from PR #25, thanks again to **@Artic0din** for the CodeRabbit audit and clean independent commits.

**Fix: `invalidate_site_info_cache()` now actually invalidates the cached payload**
The cache-invalidation helper introduced in 2.11.8 reset `_site_info_last_fetch = 0` but never cleared `_site_info_cache` itself. `async_get_site_info()` checks `if self._site_info_cache and (time.monotonic() - self._site_info_last_fetch) <= 21600`, and `time.monotonic() - 0` equals the process uptime, so on freshly-restarted HA hosts (uptime < 6 hours) the age check always passed and the stale cached payload was returned. That meant 2.11.8's fix for "stale grid export rule after write" only actually worked after 6+ hours of uptime — otherwise users saw the same stale dashboard values they had before. The cache payload is now cleared alongside the timestamp, forcing a genuine refetch on the next read regardless of uptime.

**Fix: PowerSync.cc proxy tokens no longer routed to the Teslemetry URL when restoring the export rule**
`config_flow._restore_export_rule()` ran when a user disabled solar curtailment to flip Tesla's export rule back to `battery_ok`. The provider check was a two-way if/else covering Fleet API and Teslemetry only — PowerSync.cc users (the recommended free-tier path) fell into the `else` branch and had their `psync_...` token sent to `TESLEMETRY_API_BASE_URL`, which Teslemetry's server rejected with a silent 401. Result: every curtailment-disable call silently failed and the export rule was never actually restored, leaving solar export blocked at the inverter level until manual intervention. An explicit `elif api_provider == TESLA_PROVIDER_POWERSYNC` branch now uses `POWERSYNC_API_BASE_URL` with the correct token validation.

**Fix: Fleet API provider choice now survives HA restart during initial setup**
The initial setup flow's Fleet API branch stored `self._teslemetry_data = {CONF_TESLEMETRY_API_TOKEN: ""}` — an empty token slot — but never wrote `CONF_TESLA_API_PROVIDER: TESLA_PROVIDER_FLEET_API` into the config entry data. On HA restart, `get_tesla_api_token()` read the default `TESLA_PROVIDER_TESLEMETRY`, tried to use the empty token, and 401'd on every Tesla API call. Users who picked Fleet API during setup saw everything work until the first restart, then the entire Powerwall section went stale/unknown with no obvious cause in the logs. The Fleet API dict now includes `CONF_TESLA_API_PROVIDER: TESLA_PROVIDER_FLEET_API` so the provider choice persists.

Update available via HACS
