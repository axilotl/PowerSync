<!-- release: v2.12.341 -->

## What's Changed

**Use native Solax daily energy totals**
PowerSync now reads the daily solar, grid import/export, and battery charge/discharge counters exposed by the Solax Modbus integration when they are available. This keeps the PowerSync Daily Energy card aligned with Solax's own Today values after a Home Assistant or PowerSync restart, instead of under-reporting from only the power accumulated since startup.

Update available via HACS
