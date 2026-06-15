<!-- release: v2.12.649 -->

## What's Changed

**Clean up EV price-level debug logging**
EV charging debug logs now show an unavailable current price as `unknown` instead of `Nonec`. This keeps diagnostic logs clearer when price data has not loaded yet and does not change any charging decisions.

Update available via HACS
