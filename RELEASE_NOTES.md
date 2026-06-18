<!-- release: v2.12.671 -->

## What's Changed

**EPEX import price sensor override**
PowerSync now lets EPEX users provide an optional Home Assistant sensor for actual import costs, matching the existing export price sensor override. This supports mixed tariffs where import is fixed but export remains spot-based, so optimisation decisions can use the real import price instead of wholesale EPEX import prices.

**Forecast-aware import pricing**
The new import sensor accepts the same formats as the export override: a live sensor state, positional `price_values`, timestamp-keyed `price_values`, or direct timestamp attributes. Values can be supplied in `ct/kWh` or `EUR/kWh`, and timestamped hourly values are aligned into the optimiser's 5-minute slots automatically.

Update available via HACS
