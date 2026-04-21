## What's Changed

**GoodWe Battery Curtailment**
When Battery Curtailment is enabled, GoodWe systems now correctly stop exporting to the grid during negative or near-zero export prices. Previously the curtailment check ran but had no effect on GoodWe — it fell through to the Tesla API path which does nothing for GoodWe systems. The fix uses the inverter's export limit register (set to 0W when export price < 1¢/kWh, removed when prices recover), mirroring how FoxESS and AlphaESS curtailment already works.

Update available via HACS
