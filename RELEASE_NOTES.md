<!-- release: v2.12.600 -->

## What's Changed

**Flow Power No Idle SOC stays continuous through export**
The optimiser dashboard now keeps No Idle's recalculated battery SOC on the same timeline when the plan transitions into charge or export actions. This removes stale LP SOC jumps after recalculated self-consumption periods, so the 24-hour chart and battery windows show a continuous battery path instead of snapping back to an older optimiser estimate.

Update available via HACS
