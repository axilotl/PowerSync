<!-- release: v2.12.634 -->

## What's Changed

**Restore zero grid-import cap as no cap**
PowerSync now treats Maximum grid import set to `0 kW` as no site import cap again, matching the existing setup text. Users who want Smart Optimization to avoid grid-sourced charging should use the no-grid-import/grid-charge control instead of setting the import cap to zero.

Update available via HACS
