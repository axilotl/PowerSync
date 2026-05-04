<!-- release: v2.12.278 -->

## What's Changed

**Powerwall local power now updates from the fast signed LAN feed**
Powerwall gateways can report signed v1r meter locations as uppercase labels (`BATTERY`, `SITE`, `LOAD`, `SOLAR`). PowerSync now handles those labels case-insensitively, so locally paired installs populate Battery Power, Grid Power, Solar Power, and Home Load from the signed local feed instead of falling back to slower Tesla cloud refreshes.

**FoxESS battery limits are now visible to the optimizer**
FoxESS battery setups now expose charge and discharge power limits to PowerSync, giving the optimizer the limits it needs when planning battery behavior instead of relying on missing or generic defaults.

Update available via HACS
