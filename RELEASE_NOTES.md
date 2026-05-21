<!-- release: v2.12.454 -->

## What's Changed

**Fix Smart Optimization SOC forecast below the optimiser reserve**
The Smart Optimization schedule now continues calculating the displayed SOC forecast below the optimiser backup reserve instead of flattening at the reserve line. In self-consumption periods, the forecast follows natural battery behavior from home load and solar production, so SOC drops with net household demand and rises with solar surplus while forced discharge/export remains blocked by the optimiser floor.

Update available via HACS
