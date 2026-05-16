<!-- release: v2.12.414 -->

## What's Changed

**Powerwall reserve restore fix**
PowerSync no longer saves optimizer-generated Powerwall reserve adjustments as the user's real backup reserve. This fixes cases where Smart Optimization could temporarily align reserve with the current battery SOC, then after a Home Assistant restart restore that temporary value back into the Tesla app.

**Safer Smart Optimization startup behavior**
Optimizer reserve writes are now tagged separately from user or app reserve changes, so manual backup reserve updates still persist while LP self-consumption and hold actions do not become the startup restore target.

Update available via HACS
