## What's Changed

**Solax Mode1 (RemoteControl) battery control**
Solax hybrid inverters running the modern Mode1 RemoteControl protocol can now do force charge, force discharge, and self-consumption mode through PowerSync. Previously Solax support required the legacy "manual mode" or "force time" entity families, which left Mode1 users (the most common firmware on newer X1/X3 hybrids) unable to do any forced battery action — the LP optimizer would calculate the right strategy but had no way to actually push the inverter into it. The new path detects the `remotecontrol_*` entity family, drives the inverter via the documented power/active-power/duration/trigger sequence, and falls back to the existing manual or force-time profiles when those are what the user has. Force-mode timer auto-restore is wired through, so a 10-minute force charge cleanly returns to self-use when it expires.

**Broader Solax sensor detection**
The Solax controller now recognizes a wider range of entity names from different versions of the homeassistant-solax-modbus integration: multi-battery installs (`battery_1_capacity`, `total_battery_power_charge`), triple-string PV systems (`pv3_power`), and Energy Dashboard-style sensor names (`energy_dashboard_solax_*`). If your Solax sensors weren't being picked up before, this release should detect them automatically; the auto-discovery also now scans the full HA state machine, not just the registered entities for the Solax integration entry, so unconventional installs (manually re-named entities, custom dashboards) are covered.

**Force-charge/discharge duration changes no longer trigger a full integration reload**
Adjusting the "Force Charge Duration" or "Force Discharge Duration" select entities used to fire the options-update listener and cause the entire PowerSync integration to reload — disrupting any in-flight LP optimization, force mode, or EV session in progress. The select now skips the reload when the value is unchanged and signals `_skip_reload` to the options listener when it does change, so duration tweaks are instant and don't kick off a 10-second restart cascade.

Update available via HACS
