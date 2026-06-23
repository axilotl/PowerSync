<!-- release: v2.12.706 -->

## What's Changed

**Flow Power optimizer current price alignment**
Flow Power Smart Optimization now uses the latest KWatch current interval for the active 30-minute tariff slot in the LP import price forecast. This keeps the LP price chart and optimizer inputs aligned with the canonical Current Import Price sensor and Sigenergy tariff schedule when the live wholesale interval differs from the next predispatch forecast.

**Dashboard forecast consistency**
The active Flow Power half-hour is now synthesized from the live current interval before future forecast prices are applied, so the dashboard no longer shows a stale or higher forecast value for the slot that is currently in effect.

Update available via HACS
