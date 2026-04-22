## What's Changed

**Battery Health: Stacked Powerwall Follower Units Now Show Capacity**
In multi-gateway Powerwall 3 setups, "follower" units don't expose BMS signals directly through the Fleet API and previously appeared as 0 Wh capacity in the Battery Health panel. PowerSync now infers each follower's nominal capacity and current state-of-charge by subtracting the leader pack totals from the aggregate system reading, and extracts follower serial numbers from the gateway's battery block manifest so they display correctly alongside leader packs.

**Weather Forecast: Fixed Compatibility with OpenWeatherMap and Similar Providers**
Some weather integrations only support daily forecasts rather than hourly, causing a spurious warning on every Home Assistant restart. PowerSync now reads each weather entity's declared capabilities before making the service call, automatically falls back to daily forecasts when hourly isn't available, and demotes the log to debug level for integrations that don't support forecasts at all — so the warning disappears from the HA error log.

Update available via HACS
