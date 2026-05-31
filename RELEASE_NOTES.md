<!-- release: v2.12.516 -->

## What's Changed

**EV charger limits now feed Smart Optimization correctly**
Smart Optimization now reads the per-vehicle charger settings saved by the app before building the EV load overlay. If a vehicle is configured for a lower limit such as 15A single phase, the optimizer clamps planned EV demand to that configured power instead of falling back to the 32A / 7.4kW default. This keeps the dashboard plan, battery reserve behavior, and LP forecast aligned with the actual charger capability.

**Optimizer shutdown now releases active control in monitoring mode**
When Smart Optimization is disabled or handed back to monitoring mode while it still owns an active force tariff or battery control state, PowerSync now performs the one required restore pass before monitoring mode blocks further writes. This prevents optimizer-owned control from being left behind after shutdown while preserving monitoring mode protections for normal service-level control writes.

Update available via HACS
