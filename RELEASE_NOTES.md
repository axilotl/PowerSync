<!-- release: v2.12.280 -->

## What's Changed

**Correct PW3 follower and expansion labelling**
PowerSync now uses the BMS pack scan together with Tesla's Powerwall base-unit count so a site with one leader PW3, one follower PW3, and expansion packs is shown as `Leader PW3`, `Follower PW3`, then `Expansion Pack 1`, `Expansion Pack 2`, instead of treating the follower as another expansion.

**Remove old standalone pack devices**
Pack-level sensors continue to live under the aggregate `Tesla Powerwall` device, and legacy standalone `Powerwall 1` / `Powerwall 2` pack devices from the earlier release are cleaned up on integration load.

Update available via HACS
