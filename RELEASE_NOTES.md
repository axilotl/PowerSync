## What's New

### Off-Grid Curtailment in the Optimizer
The LP optimizer can now physically take your Powerwall off-grid during negative export price periods. When enabled in Battery Setup > Local Control, the optimizer identifies periods where export has zero or negative value and marks them as OFF_GRID in the schedule. The Powerwall physically disconnects from the grid, guaranteeing zero export — stronger than Tesla's "never export" rule alone.

The optimizer coordinates off-grid timing with charge/discharge planning so it automatically reconnects before any upcoming charge window. Solar continues producing while off-grid, charging the battery and powering your home.

Safety gates: minimum SOC floor (default 40%), daily duration cap (default 6 hours), minimum 15 minutes per off-grid session to prevent contactor cycling.

**Requires:** Tesla Powerwall with completed gateway pairing + off-grid curtailment enabled. No change for users who don't enable this feature — the optimizer continues using Tesla's export rule as before.

### Grid Status Notifications Fixed
Grid outage/restored push notifications no longer fire on every HA restart. They only trigger on actual grid transitions and correctly distinguish between Active (on-grid) and Inactive (off-grid) states.

Update available via HACS
