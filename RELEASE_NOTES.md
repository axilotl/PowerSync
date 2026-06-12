<!-- release: v2.12.622 -->

## What's Changed

**Fix Solcast Solar forecast loading**
PowerSync now correctly awaits asynchronous forecast lists exposed by newer Solcast Solar integrations. This prevents the solar forecast loader from dropping back to a zero-solar forecast when Home Assistant reports that `SolcastApi.get_forecast_list` was never awaited.

Update available via HACS
