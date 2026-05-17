<!-- release: v2.12.416 -->

## What's Changed

**Clarified Amber export-price timing**
PowerSync now keeps date context on rolling TOU schedule entries so app clients can distinguish today's slots from tomorrow's slots. This avoids comparing the wrong Amber export period when the next-24-hour schedule wraps past midnight.

**Date-aware price spike alerts**
Import and export spike push notifications now show clear timing such as Today or Tomorrow instead of only a clock time. The alert dedupe key also uses the full spike timestamp so same-time alerts on different days are handled separately.

**Improved Powerwall 3 expansion mapping**
PowerSync now reconciles PW3 expansion and follower pack roles more reliably when Home Assistant receives partial or serial-less battery block data, improving the accuracy of exposed pack-level battery health entities.

Update available via HACS
