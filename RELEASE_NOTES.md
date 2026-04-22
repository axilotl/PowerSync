## What's Changed

**Native Update Notifications in Home Assistant**
PowerSync now registers as a native HA update entity, so new releases appear directly in **Settings → System → Updates** alongside core HA and HACS updates. HA polls the GitHub Releases API hourly and shows the installed vs latest version, with a link to the release page and the full release notes when you tap the entry. GitHub API rate limiting is handled gracefully — if the hourly check is throttled, it silently retries next cycle without raising errors.

**Battery Mode Sensor Now Reflects Hold SOC and Self-Consumption State**
The Battery Mode sensor reads hold-SOC and self-consumption state when determining the current mode, but wasn't subscribed to the dispatcher signals that fire when those modes activate or deactivate. The sensor would display a stale value until something else (like a force-charge event) triggered a refresh. It now subscribes to `hold_soc_state` and `self_consumption_state` signals and updates immediately when either mode changes.

**Weather Errors at Startup When Entities Are Unavailable**
If all configured weather entities are in an `unknown` or `unavailable` state — common during HA startup or when a weather provider is temporarily down — the integration now skips them cleanly and returns no weather data rather than crashing with a string operation error. The first healthy entity found is used; if none are available, the weather resolver returns `None` and retries on the next cycle.

**Per-Vehicle Minimum Charging Power**
EV chargers configured through smart charging coordination can now have different minimum charging power thresholds. Previously all vehicles used a hardcoded 1400W floor, which is too high for some EVs and too low for others. The `min_power_w` parameter defaults to 1400W (no change for existing users) but can now be set per vehicle. Values are validated on registration — zero, negative, or values exceeding the vehicle's maximum are rejected with an error log.

**API Responses No Longer Leak Internal Error Details**
HTTP error responses from the local Powerwall API views and the weather settings endpoint previously included raw Python exception messages, which could expose internal details such as connection strings or file paths to API consumers. Generic user-safe messages are now returned instead, while full tracebacks continue to be recorded in the HA log via `_LOGGER.exception()` for debugging.

Update available via HACS
