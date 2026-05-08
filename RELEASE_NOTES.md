<!-- release: v2.12.339 -->

## What's Changed

**Fix Zaptec charger state parsing**
Zaptec standalone mode now reads charger state observations using Zaptec's documented IDs. Charger operation mode comes from `710`, phase currents remain on `507`, `508`, and `509`, session energy comes from `553`, and firmware version comes from `911`. This prevents command IDs and observation IDs from being mixed up, keeping Zaptec charging status, power, and session reporting aligned with the live Zaptec API constants.

Update available via HACS
