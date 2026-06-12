<!-- release: v2.12.633 -->

## What's Changed

**Zero grid-import cap for optimizer charge planning**
PowerSync now treats a configured Maximum grid import of `0 W` as a real zero-import cap instead of the same as an unset cap. This stops Smart Optimization from planning grid-sourced force-charge slots when users have explicitly set the site import cap to zero, while still allowing any charge that can be supplied by genuine solar surplus.

Update available via HACS
