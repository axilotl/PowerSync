<!-- release: v2.12.675 -->

## What's Changed

**Stop flooding the log with Tesla tariff warnings on non-Tesla systems**
On battery systems without Tesla energy configured (Sungrow, FoxESS, Sigenergy, etc.), PowerSync logged "Missing Tesla site ID or token for tariff fetch" on every poll — thousands of spurious warnings a day that buried real issues. It now only warns when a Tesla energy site is configured but its token is missing, and stays quiet otherwise. No change for Tesla setups.

**Fill the midnight price gap when a provider publishes it late**
Some providers (e.g. Flow Power's kwatch source) don't publish the 00:00-00:30 price until around midnight, so PowerSync logged "PERIOD_00_00: No price data available" repeatedly from ~23:30 and left that first slot empty. It now backfills the leading unpublished period(s) from the first available price (consistent with the existing forecast-gap fallback), removing the gap and the warning flood.

Update available via HACS
