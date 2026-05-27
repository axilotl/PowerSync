<!-- release: v2.12.487 -->

## What's Changed

**GoodWe export power refresh**
PowerSync now refreshes an active optimizer-owned export command when the LP target power changes inside the same export mode. This fixes GoodWe EMS sites that could stay pinned to an older lower export limit, such as a previous 2.2kW command, even after Smart Optimization moved the current target up to a higher value.

**Target-power systems only**
The refresh is limited to battery systems that support target charge/export power commands, so non-target systems keep the existing force-mode extension behavior.

Update available via HACS
