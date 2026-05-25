<!-- release: v2.12.470 -->

## What's Changed

**Load forecast startup selection**
PowerSync now ignores generated forecast and prediction sensors when auto-selecting a home load source for Smart Optimization. This prevents startup races where the optimizer selected `sensor.powersync_home_load_forecast`, saw no recorder history, and kept the load forecast at 0 W until a manual reload.

**Flow Power TWAP tracking on FoxESS**
Flow Power wholesale samples are now recorded before battery-specific tariff routing. FoxESS + Flow Power systems will build the rolling 30-day TWAP normally instead of repeatedly falling back to the default 8.00 c/kWh value after restarts or upgrades.

Update available via HACS
