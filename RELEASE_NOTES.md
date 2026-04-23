## What's Changed

**Optimizer reserve: battery no longer drains below the configured backup reserve**
A cascading drain bug was causing batteries to discharge well below the optimizer reserve when SOC dropped below that threshold. The LP optimizer was setting its working floor to `current SOC − 1%` each cycle, allowing 1% further discharge per 5-minute LP run — resulting in 3%+ drops per cycle as seen in reports (28% → 25% → 22% → 19%). The floor is now fixed at the current SOC (no further discharge allowed), and the optimizer coordinator now blocks any EXPORT action outright when SOC is at or below the configured reserve. For GoodWe systems specifically, the ECO_DISCHARGE `soc_floor` parameter is now passed the backup reserve value so the hardware enforces the same minimum SOC on its end.

**AEMO: LP re-optimization no longer fires on every 1-second poll**
The AEMO price coordinator switches to 1-second polling when searching for a new dispatch file. HA fires all registered listeners on every successful poll, which was triggering a full LP re-optimization run every second during that window — a significant waste of CPU that could also cause the LP to produce a slightly different schedule each cycle due to floating-point timing differences. Re-optimization now only runs when the `dispatch_file` key in the AEMO data actually changes, so the LP fires once per new dispatch interval rather than hundreds of times.

**Battery health: live and stored data are now merged by timestamp (Tesla)**
The battery health system now compares the timestamps of the live cloud-fetched BMS result and any stored WiFi-scan result, presenting whichever is newer rather than blindly preferring one source. Live BMS results are also written back to the HA sensor store immediately so they survive restarts without needing another refresh. Previously, a fresh BMS fetch could be silently discarded if older stored data was already present.

*Update available via HACS*
