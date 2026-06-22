<!-- release: v2.12.690 -->

## What's Changed

**Scheduled EV preserve keeps the Powerwall no-discharge hold active**

PowerSync no longer lets the optimizer polling safety check restore the Tesla backup reserve while a scheduled EV preserve no-discharge hold is still active. This keeps the Powerwall held during EV preserve windows instead of internally marking no-discharge as active while the hardware reserve has already been restored.

Update available via HACS
