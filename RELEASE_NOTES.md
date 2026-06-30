<!-- release: v2.12.740 -->

## What's Changed

**No Idle status display**
No Idle mode now shows the same effective `self_consumption` action in the optimizer status and action-plan API that PowerSync already applies at runtime. This fixes cases where monitoring mode, external-control setups, or dashboard automations saw `idle` in `sensor.power_sync_optimization_status` even though No Idle mode had converted that slot to self-consumption.

Update available via HACS
