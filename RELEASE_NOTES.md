## What's Changed

**Flow Power: Tariff Code Dropdown No Longer Blocks Saving**
When a DNSP was selected and actual tariff codes were loaded, the empty "skip" option was removed from the dropdown — making the tariff code effectively required and preventing the form from saving. A "skip" option is now always present at the top of the list, so users who don't need a specific tariff code can proceed without selecting one.

**Dashboard: Tesla Energy Site Section Hidden for Non-Tesla Setups**
The "⚡ Tesla Energy Site" controls card (backup reserve, operation mode, grid export, grid charging, storm watch) was appearing on dashboards for GoodWe, FoxESS, Sigenergy, and other non-Tesla battery systems. The entity search used to find Tesla controls was matching entities from unrelated integrations by suffix. The section is now gated on PowerSync-specific Tesla entities (`power_sync_backup_reserve` / `power_sync_operation_mode`), and the entity search fallback is restricted to Tesla/Powerwall-related entity IDs only.

Update available via HACS
