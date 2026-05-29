<!-- release: v2.12.498 -->

## What's Changed

**Smart Optimization settings save without modal timeouts**
PowerSync now lets the Home Assistant Smart Optimization options dialog finish saving before reloading the integration in the background. This avoids the greyed-out settings popup and generic "Unknown error occurred" banner that could appear when changing Profit Max or other Smart Optimization settings on slower reloads.

**Flow Power network tariff dropdowns populate again**
Flow Power tariff selection now reads network tariff codes through the current `aemo-to-tariff` lookup API while keeping compatibility with older tariff modules. Queensland and other networks that no longer expose the legacy tariff map now show their available tariff codes instead of only `None`, so users can select the DNSP tariff from their bill.

Update available via HACS
