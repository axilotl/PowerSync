<!-- release: v2.12.401 -->

## What's Changed

**GoodWe EMS restore no longer keeps stale power limits**
When PowerSync restores a GoodWe system using the GoodWe HA EMS entity bridge, it now clears the EMS power limit before switching the inverter back to `auto`. This prevents a previous forced charge or export limit from lingering after `restore_normal`, which could leave the inverter exporting after PowerSync had released control.

Update available via HACS
