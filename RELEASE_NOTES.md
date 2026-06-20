<!-- release: v2.12.681 -->

## What's Changed

**Protect Globird VPP startup from cancelled AEMO fetches**
PowerSync now runs the first Globird/AEMO VPP spike-price check in the background instead of awaiting it during Home Assistant config entry setup. If Home Assistant cancels a slow startup network request, the integration no longer risks being left partially set up with platforms already registered, which could prevent later tariff/export automation from running normally.

**Clean VPP spike timers on unload**
The Globird VPP AEMO timer and first-run task are now cancelled during unload/reload so a restart does not leave stale spike-check callbacks behind.

Update available via HACS
