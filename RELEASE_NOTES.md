<!-- release: v2.12.486 -->

## What's Changed

**Refresh Powerwall pack energy automatically**
PowerSync now refreshes Tesla Powerwall BMS battery-health data every 5 minutes for locally paired Powerwall sites, so pack-level current energy sensors update without waiting for a manual app battery-health scan. The polling path skips overlapping requests and shuts down cleanly when the integration unloads.

**Leave room for forecast solar in Flow Power Profit Max**
Flow Power Profit Max now accounts for forecast net solar before the Happy Hour target time when planning prefill. The optimiser still targets the configured SOC before the export window, but avoids grid-charging above a solar-aware ceiling when Solcast and load forecasts show that afternoon solar can finish the battery charge.

Update available via HACS
