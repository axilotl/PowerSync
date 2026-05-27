<!-- release: v2.12.485 -->

## What's Changed

**Keep solar surplus EV charging available below the battery threshold**
Solar surplus EV charging can still start below the configured home battery minimum when there is true surplus left after reserving the configured battery charge power. The Smart Schedule solar-surplus path now follows the same rule, with clearer reasons when charging is blocked because the remaining surplus is not enough after the battery reserve.

**Stop unscheduled external EV charging**
Scheduled Charging now detects an already-active external EV charge session outside the configured schedule and stops it through the coordinated EV stop path. This prevents a charger that was started elsewhere from continuing when the scheduled charging policy says it should be inactive.

Update available via HACS
