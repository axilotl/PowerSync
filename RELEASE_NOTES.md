<!-- release: v2.12.717 -->

## What's Changed

**Tesla SOC fallback during partial live-status polls**
Tesla/Fleet live status can occasionally return a wall-connector-only payload without `percentage_charged`. PowerSync now keeps the last valid Powerwall SOC instead of treating the missing field as `0%`, preventing Smart Optimization from planning unnecessary expensive grid-charge windows when Tesla temporarily omits the battery percentage.

Update available via HACS
