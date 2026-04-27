## What's Changed

**SAJ H2: AppMode Written Before Passive Enable (Register Write Order Fix)**
When entering passive charge, passive discharge, or idle mode, AppMode was being written to the stanus74 command queue *after* `passive_charge_enable`. Stanus74's number entity handler writes `passive_charge_enable` directly to the Modbus register without touching AppMode, so the inverter was receiving the passive enable instruction while still in its previous mode (e.g. TOU), causing erratic passive mode entry. AppMode=3 is now queued first so the inverter enters passive mode cleanly before the charge/discharge direction register is set.

**SAJ H2: Safety Guards on Force Charge/Discharge/Idle**
Three protections added to prevent unsafe or incomplete passive mode transitions. A pre-flight check now verifies that the `passive_enable` and `app_mode` number entities are mapped before any operation begins — previously, a missing entity would silently leave the inverter in AppMode=3 with no passive direction set. Force discharge now refuses to run when battery SOC is at or below 10%, since manual commands bypass the LP optimizer's safety rails. If a write sequence fails mid-way after AppMode=3 has been sent, `restore_normal` is automatically called to recover the inverter to a clean state.

Update available via HACS
