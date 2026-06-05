<!-- release: v2.12.592 -->

## What's Changed

**Profit Max export windows keep today's battery available**
PowerSync now scopes the auto-applied home-load export floor to the export window it was calculated for. This prevents a reserve floor needed for a future day's load forecast from prematurely clamping today's Flow Power Happy Hour export window, while still protecting the later window when that day becomes current.

Update available via HACS
