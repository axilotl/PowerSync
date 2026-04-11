## What's Changed

**Fix: Tesla Energy Site controls now actually appear on the dashboard**
The auto-generated dashboard's "Tesla Energy Site" section was only finding `switch.grid_charging` on most installations, leaving the rest of the battery controls (backup reserve, operation mode, grid export rule, storm watch, off-grid EV reserve, VPP programs, status sensors) invisible. The cause: the entity finder only scanned `hass.states` and used a narrow suffix match that could miss entities created under non-default device names. It now also scans the HA entity registry (`hass.entities`), which includes registered-but-currently-unavailable entities, and has a diagnostic `console.debug` so if anything is still missing you can see exactly which entity id wasn't found in your browser console.

**Refresh: battery controls are now real control tiles, not a plain list**
The "Tesla Energy Site" section has been redesigned from a plain entities list into a stacked grid of HA tile cards grouped by type — sliders for reserve percentages, selects for operation mode and grid export rule, toggles for grid charging / storm watch / VPP program enrollment, and a compact status row for storm-watch-active and manual-export-override. Each control is a distinct visual widget so all the Powerwall settings PowerSync exposes show up as proper controls next to the existing force charge/discharge/restore panel, matching the user request that battery controls "should be shown as controls".

Update available via HACS
