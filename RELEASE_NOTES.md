<!-- release: v2.12.563 -->

## What's Changed

**Fix: toggling EV integration from the Home Assistant UI now reconnects smart charging**
After the recent change that made optimiser settings apply instantly without a reload, turning EV integration on or off from Home Assistant's settings only flipped an internal flag — it didn't actually start or stop the EV charging coordinator. That meant the optimiser would account for EV load in its battery plan but wouldn't coordinate when the car charged. EV integration changes now trigger a proper reload so the EV charging coordinator is fully wired up. (Changing other optimiser settings still applies instantly with no reload; the mobile app is unaffected.)

Update available via HACS
