<!-- release: v2.12.588 -->

## What's Changed

**Profit Max target time reloads cleanly**
PowerSync now stores the Profit Max target time on the running optimizer coordinator and restores it during startup or integration reload. This prevents Flow Power Profit Max from waiting for a manual target-time change before recalculating the plan after an update or reload.

**Sungrow restore-normal failure handling**
Sungrow restore-normal now keeps the force-mode state active when the inverter restore call fails or the coordinator is unavailable, and surfaces a Home Assistant notification instead of silently clearing the state. The optimizer also detects when Sungrow still reports forced mode while the LP plan has returned to self-consumption and reapplies restore-normal.

Update available via HACS
