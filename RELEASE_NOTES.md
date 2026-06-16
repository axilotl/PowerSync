<!-- release: v2.12.657 -->

## What's Changed

**Fix Fronius/BYD AC inverter containment**
PowerSync now runs configured AC inverter curtailment for non-Tesla battery entries instead of exiting early when no Tesla export-rule token is available. This fixes Fronius GEN24/BYD setups where the optimizer detected a full battery and low export value, but the Fronius inverter containment path was skipped until an external script changed the export limit.

**Improve Fronius load-following refresh**
Fronius AC inverter curtailment now participates in the same load-following refresh loop as other export-limit capable inverters, so the export limit can keep tracking home load while containment is active.

Update available via HACS
