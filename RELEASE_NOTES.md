<!-- release: v2.12.455 -->

## What's Changed

**SolarEdge AC and export curtailment support**
PowerSync can now control SolarEdge inverters for negative feed-in events using direct Modbus TCP active-power limiting, with a Home Assistant entity fallback for existing SolarEdge Modbus setups. SolarEdge is available as an AC inverter brand and as a SolarEdge curtailment-capable system, with rated AC power configuration so load-following curtailment can be converted into the inverter's 0-100% active power limit.

**Scheduled EV charging can preserve the home battery**
Scheduled EV charging now has a preserve-home-battery intent that tells the optimiser to block home-battery discharge while still allowing charging. This prevents EV charging sessions from draining the home battery during the scheduled window, and restores the normal inverter mode after the preserve request clears.

**Scheduled charging end times are now exclusive**
Scheduled EV charging windows now stop exactly at the configured end time instead of treating the end minute as still inside the schedule. Overnight schedules follow the same rule, avoiding one extra charging cycle at the boundary.

Update available via HACS
