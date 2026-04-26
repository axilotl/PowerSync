## What's Changed

**Automations now execute regardless of monitoring mode**
In v2.12.163, battery and grid control actions in PS automations (set_backup_reserve, set_operation_mode, set_grid_charging, etc.) were blocked when the optimizer was in monitoring mode. This was incorrect — monitoring mode is intended to keep the *optimizer* from making autonomous changes so you can observe its decisions, but user-configured automations should always run. Time-triggered automations set to fire at 10AM, 2PM, etc. were silently skipped. This is now fixed.

Update available via HACS
