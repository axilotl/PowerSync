## What's Changed

**Solax Hybrid battery system support**
Solax X1/X3 Hybrid Gen4, Gen5, Gen6, and AC Retro-Fit inverters are now supported as a full battery system — charge/discharge control, SOC metering, backup reserve, and LP optimizer participation. PowerSync connects via the [wills106/homeassistant-solax-modbus](https://github.com/wills106/homeassistant-solax-modbus) integration (install from HACS first), reading sensors and writing control entities rather than opening a direct Modbus connection. This avoids the one-master restriction of the Solax PocketWiFi dongle and keeps your existing solax_modbus setup running unchanged. Select **Solax Hybrid** in the battery system picker during setup.

**Solax setup: smarter prefix detection and clearer errors**
When configuring the entity prefix, PowerSync now scans your HA states for the wills106 fingerprint entity (`select.*_charger_use_mode`) and pre-fills the prefix automatically if a unique match is found. If the prefix is wrong, the error now names the first missing entity — e.g. *"The first missing entity was: select.solax_modbus_charger_use_mode"* — so you can immediately see what prefix to use rather than hunting through Developer Tools. This matters because users with multiple Solax integrations installed will have a different prefix than the default `solax`.

**Grid export control for GoodWe and AlphaESS**
The "Set Grid Export Rule" service (`never` / `battery_ok` / `pv_only`) now works correctly for GoodWe and AlphaESS battery systems. Previously, GoodWe returned an error response and AlphaESS was silently ignored. Both now map the export rule to their respective hardware registers — GoodWe via `REG_EXPORT_LIMIT` and AlphaESS via `REG_MAX_FEED_INTO_GRID_PERCENT`. The `/api/power_sync/powerwall_settings` endpoint also now returns a proper success response for both, with the current `grid_export_rule` derived from curtailment state, so the app can display the correct toggle state.

Update available via HACS
