<!-- release: v2.12.582 -->

## What's Changed

**Auto Reserve export plans now stop at the home-load bridge floor**
Smart Optimization now feeds the Auto Reserve home-load export floor back into the optimiser as an export-only reserve floor. This keeps profitable charge/export arbitrage available while preventing planned battery export from draining below the reserve needed to cover forecast home load after the export window.

**Dashboard plans now match export execution guards**
The optimizer plan and reserve recommendation are recalculated together after the export-only floor is discovered, so the dashboard no longer shows export continuing to the hardware reserve when execution would stop earlier for the home-load bridge. The same export guard now applies whenever Auto Reserve is enabled, with or without Profit Max.

Update available via HACS
