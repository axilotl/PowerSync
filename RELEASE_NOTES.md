## What's Changed

**GoodWe: IDLE mode no longer ignores forced charge/discharge**
When the LP optimizer issued an IDLE command to a GoodWe battery that was previously in ECO_CHARGE or ECO_DISCHARGE mode, the inverter would stay in that mode indefinitely — the DOD floor register was being updated but the operation mode was never changed. IDLE now calls `restore_normal()` first to return the inverter to GENERAL mode before setting the SOC hold floor. A Tesla-specific 80% SOC cap that was incorrectly being applied to GoodWe's DOD register has also been removed.

**GoodWe / all batteries: optimizer IDLE was being blocked by a bad heuristic**
A median-price override was preventing IDLE from executing whenever the current import price was at or above the median, on the incorrect basis that "holding the battery wastes grid import." IDLE doesn't import from grid — it just prevents battery discharge so the battery can be held for an upcoming export spike. The LP optimizer had already weighed self-consumption against future export value and chosen to hold; this secondary check was overriding that decision every cycle. Removed entirely. The LP's IDLE decisions are now respected.

**ESY Sunhome: IDLE mode was silently force-charging from grid**
A serious bug where the optimizer's IDLE action was triggering Emergency Mode on ESY Sunhome inverters — which is force-charge-from-grid. Every LP-scheduled IDLE period was instead charging the battery from grid at full rate. Fixed by removing the incorrect `set_backup_mode` → Emergency Mode mapping; IDLE now correctly sets Regular Mode.

**SAJ H2 / ESY Sunhome: service call errors during optimizer actions**
The `set_self_consumption`, `set_backup_reserve`, and `set_autonomous` service handlers had no branches for SAJ H2 or ESY Sunhome, causing all three to fall through to the Tesla Powerwall path and log "Missing Tesla site ID or token" errors on every optimizer cycle. All three handlers now have explicit SAJ and ESY branches.

**Solax: config entry bridge (Gen4/Gen5/Gen6 compatibility)**
The Solax battery bridge has been reworked to use config entry-based entity discovery, matching the approach used by SAJ H2 and ESY Sunhome. This fixes setup failures on Gen4/Gen5/Gen6 firmware where `battery_minimum_capacity` was renamed to mode-specific entities (`inverter_selfuse_discharge_min_soc`, `inverter_selfuse_backup_soc`). Connection is now discovered automatically from the selected config entry rather than requiring a host address.

**Dashboard: new weather scenes (cloudy, snow, storm)**
The energy flow dashboard now shows weather-appropriate backgrounds for cloudy, snow, and storm conditions in addition to the existing clear and rain scenes. Previously these conditions fell back to a default background. Night variants are included for all new weather types.

**Dashboard: idle grid line visibility in dark scenes**
Grid import/export lines were not rendering correctly during idle state when using night/dark scene backgrounds. Fixed.

**Automation actions: no more spurious failure alerts on non-Tesla systems**
`set_grid_export` and `preserve_charge` automation actions were returning failure when called on non-Tesla hardware, triggering "Automation Action Failed" push notifications even though nothing had gone wrong — those actions simply don't apply to other battery systems. They now return silently skipped so automations can be shared across Tesla and non-Tesla installs without alerts.

*Update available via HACS*
