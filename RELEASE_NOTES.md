<!-- release: v2.12.351 -->

## What's Changed

**Electricity price graph axis labels restored**
PowerSync now applies the cents/kWh chart multiplier consistently when drawing dashboard price graphs. The Electricity Prices and TOU Schedule cards no longer collapse every y-axis label to `0c/kWh` while the plotted price lines and legend values show non-zero prices.

**Dashboard cache refreshed**
The dashboard JavaScript cache-bust version was bumped so Home Assistant requests the corrected strategy bundle after updating through HACS.

Update available via HACS
