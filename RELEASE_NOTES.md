<!-- release: v2.12.464 -->

## What's Changed

**Monitoring Mode switch stays in sync**
Turning Monitoring Mode on or off from the PowerSync app now updates the matching Home Assistant switch state immediately. The switch also reads the current config-entry option instead of relying on a startup-only cached value, so the dashboard cannot show Monitoring Mode as enabled while Smart Optimization is already allowed to control the battery.

Update available via HACS
