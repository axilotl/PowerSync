<!-- release: v2.12.382 -->

## What's Changed

**Recover cleanly from Tesla Fleet token expiry**
PowerSync now treats expired Tesla Fleet API tokens as a transient upstream refresh condition instead of marking the PowerSync integration itself as needing reauthentication. This prevents Tesla Powerwall sites using the Home Assistant Tesla Fleet integration from stopping after a short-lived token expires, while direct PowerSync and Teslemetry tokens still trigger the normal reauth prompt when they are rejected.

Update available via HACS
