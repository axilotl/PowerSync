<!-- release: v2.12.340 -->

## What's Changed

**Align optimizer polling with tariff boundaries**
Smart Optimization now re-runs on wall-clock interval boundaries instead of drifting by the time taken by the previous LP solve. This keeps scheduled battery actions aligned with tariff changes such as Flow Power Happy Hour export windows, so a price step at 17:30 is picked up at 17:30 rather than several minutes later.

Update available via HACS
