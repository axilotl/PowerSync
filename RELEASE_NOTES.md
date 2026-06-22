<!-- release: v2.12.685 -->

## What's Changed

**Flow Power base rate fix for Smart Optimization**
Smart Optimization now uses the configured Flow Power base rate even when that value was saved during initial setup rather than later options editing. This keeps optimiser import prices aligned with the Flow Power price sensors and avoids falling back to the old 34.0c/kWh default when a plan uses a different base rate.

Update available via HACS
