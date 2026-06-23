<!-- release: v2.12.705 -->

## What's Changed

**Flow Power optimizer import forecasts**
Flow Power Smart Optimization now applies forecast-confidence damping to far-future import price spikes while preserving the fixed Happy Hour export schedule. This prevents speculative next-day predispatch spikes from dominating the LP plan unchanged and producing extreme charge/export decisions, without changing the displayed tariff schedule or the live/current price sensors.

**Happy Hour export planning preserved**
The optimiser still treats Flow Power Happy Hour export as the contractual fixed export window, so Profit Max can continue planning around valid export opportunities while import-side wholesale forecasts remain uncertainty-adjusted.

Update available via HACS
