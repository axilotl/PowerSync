<!-- release: v2.12.558 -->

## What's Changed

**Home Assistant no longer freezes while PowerSync starts up**
When PowerSync loaded, the optimiser's first forecast crunched a month of home-load history (often hundreds of thousands of data points) and fitted its temperature model directly on Home Assistant's main loop — briefly freezing the whole UI until it finished. That heavy number-crunching now runs on a background thread, so Home Assistant stays responsive while PowerSync warms up. The database read was already in the background; this moves the remaining processing and the temperature fit off the main loop too. Combined with the faster HiGHS solver and the smarter startup timing from recent releases, startups are noticeably smoother.

Update available via HACS
