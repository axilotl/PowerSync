<!-- release: v2.12.354 -->

## What's Changed

**Smarter load forecasts for new installs**
PowerSync now avoids repeating the same load profile across every forecast day when only partial home-load history is available. If a future day is missing exact day-of-week history, the LP optimizer now falls back to matching weekday or weekend history first, instead of averaging all available days into one repeated shape.

Update available via HACS
