<!-- release: v2.12.605 -->

## What's Changed

**Profit Max reserve protection**
Profit Max plans now preserve pre-export battery holds when No Idle mode is enabled, handle target times that do not land exactly on a 5-minute optimiser boundary, and prevent forced export actions from being displayed or dispatched below the configured optimiser reserve. This fixes plans that could show a Happy Hour export draining below the reserve even when the user had set a manual optimiser floor.

**Force-discharge refresh for supported non-Tesla batteries**
Optimizer-owned force-discharge windows now re-issue the hardware command when telemetry shows the inverter has stayed in self-consumption instead of entering a sell/export mode. This helps GoodWe-style systems recover from stale export commands during active optimizer export windows.

**Optimizer plan rendering**
The 24-hour optimizer plan card now avoids rebuilding the chart on unrelated Home Assistant state updates, while still refreshing for relevant price, force-charge, and force-discharge changes. This should make the plan card feel steadier on busy dashboards.

Update available via HACS
