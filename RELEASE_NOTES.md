<!-- release: v2.12.601 -->

## What's Changed

**Profit Max export now respects reserve without Spread Export**
Flow Power Profit Max plans now keep forced export actions above the configured optimiser reserve even when Spread Export is turned off. Starting below the optimiser reserve can still allow normal self-consumption down to the hardware floor, but once the plan charges back up and schedules an export window it will not use the hardware reserve as the export floor.

Update available via HACS
