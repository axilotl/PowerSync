## What's Changed

**Fix: GRID CONNECTED text no longer overlaps the export value in the energy flow card**
Thanks to Barbars for the report. The auto-generated PowerSync dashboard's Tesla-style energy flow card had a layout bug where the "CONNECTED" / "OFF GRID" status text rendered at its default SVG position while the scene-specific themes moved the GRID label and kW value around it — causing the status text to overlap the grid power value in most of the 12 scene layouts. The status text is now wired into the theme system and automatically positioned 15 pixels below whichever y-coordinate each theme chose for grid power, matching the spacing of the default layout.

**Fix: Mobile app now shows grid status (on-grid / off-grid banner and flow label)**
The app relies on the backend config endpoint (`/api/power_sync/backend_config`) to resolve real Home Assistant entity IDs, since HA now composes them from the device name rather than the suggested object_id. The resolution list was missing `grid_status` and `firmware`, so the mobile app fell back to `sensor.power_sync_grid_status` — which doesn't exist on installations where the PowerSync device is named something else. The app never saw the grid status and never displayed the off-grid banner or switched the flow label to "OFF GRID", even during actual outages. Both keys are now resolved correctly.

Update available via HACS
