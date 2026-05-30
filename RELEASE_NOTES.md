<!-- release: v2.12.510 -->

## What's Changed

**Monitoring mode now blocks all battery control writes**
Monitoring mode now acts as a hard stop across the adjacent control paths as well as the obvious force charge and force discharge services. This prevents optimizer cleanup, persisted force-mode replay after restart, backup-reserve changes, hold SoC, operation-mode writes, grid export, grid charging, Storm Watch, off-grid EV reserve, and VPP enrollment commands from touching hardware while PowerSync is meant to observe only.

**Smart Schedule preserves future EV charging demand**
Smart Schedule now keeps a valid charging plan for an away or unplugged vehicle when that vehicle still has a future deadline. The home-battery optimizer can reserve energy for the upcoming EV demand without sending charger commands until the vehicle is actually available, and stale plans are cleared once the target SoC is already reached.

Update available via HACS
