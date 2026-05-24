<!-- release: v2.12.462 -->

## What's Changed

**Safer Tesla optimizer force discharge**
PowerSync now treats optimizer-owned force modes from a Home Assistant restart as stale while they are being cleaned up, so Smart Optimization cannot extend an old force-discharge state during startup. Tesla force discharge also disables grid charging before uploading the high-export tariff, preventing a Powerwall from importing from the grid while PowerSync is trying to force discharge.

**Sigenergy EVDC charger handling**
Sigenergy EVDC chargers now use conservative one-shot control instead of unsupported dynamic amp updates. PowerSync exposes EVAC/EVDC capability flags to mobile, blocks repeated EVDC restarts until an unplug/replug is observed, and hands EVDC solar-surplus behavior back to native mySigen PV-surplus handling while continuing to monitor charging state.

**Improved SAJ H2 and Solax solar telemetry**
SAJ H2 and Solax integrations now prefer the summed PV-string power when the reported total solar value is partial. SAJ H2 also forwards per-string PV power and daily solar/import/export energy into PowerSync summaries for more accurate dashboard and history data.

Update available via HACS
