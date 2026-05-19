<!-- release: v2.12.433 -->

## What's Changed

**Fixed AC inverter setup from the options menu**
PowerSync now enables the AC-coupled inverter polling path when users configure a separate inverter from the AC inverter options menu. This fixes cases where the SG/Fronius/GoodWe/etc. inverter details appeared to be saved, but runtime status still reported "Inverter curtailment not enabled" and the extra AC solar output was missing from the dashboard.

Update available via HACS
