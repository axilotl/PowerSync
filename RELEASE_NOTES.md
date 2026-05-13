<!-- release: v2.12.397 -->

## What's Changed

**Fix phantom Tesla EV power in Home Assistant**
PowerSync now ignores stale Tesla and Teslemetry EV power readings when the vehicle is disconnected, away from home, or only in an idle connected state. This prevents the Home Assistant EV power sensor and built-in energy-flow dashboard from showing usage from a Tesla that is not actually home or plugged in.

**Keep real charger telemetry working**
Wall Connector telemetry and actively charging Tesla vehicles still report measured EV power as before, while disconnected vehicle sensors no longer get treated as home load or active charging.

Update available via HACS
