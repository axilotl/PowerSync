<!-- release: v2.12.304 -->

## What's Changed

**Fix Sigenergy tariff upload prices**
Sigenergy tariff uploads now build the 48-slot static plan from the next 24 hours instead of averaging Amber prices that share the same clock time across different dates. This prevents past settled prices from being mixed with tomorrow's forecast and keeps the figures shown in the Sigenergy app aligned with the expected Amber schedule.

Update available via HACS
