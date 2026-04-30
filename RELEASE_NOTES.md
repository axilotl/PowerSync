## What's Changed

**Hold SoC button added to the Home Assistant dashboard**
The PowerSync dashboard now has a dedicated "Hold SoC" button (blue, battery-lock icon) sitting beside the Restore button under the battery controls. Tapping it calls `power_sync.hold_battery_soc` for the duration selected on the discharge chip — locking the battery at its current state of charge so it neither charges nor discharges until the timer expires (or you tap Restore). Previously this primitive was only reachable from the mobile app; now it's a one-tap control directly from the HA Lovelace dashboard.

Update available via HACS
