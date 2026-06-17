<!-- release: v2.12.667 -->

## What's Changed

**Keep Sigenergy grid export separate from ESS discharge capacity**

Sigenergy force discharge now leaves enough ESS discharge headroom for current home load while still setting the grid export target and export limit to the requested export amount. This prevents household consumption from consuming the whole battery discharge allowance and stopping the intended grid export during ZeroHero and other export windows.

Update available via HACS
