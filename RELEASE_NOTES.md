## What's Changed

**Powerwall SOC now matches the Tesla app again (regression fix from v2.12.248)**
The local-TEDAPI SOC reading has been over-reading by about 4% since v2.12.248. That release refactored the four-call TEDAPI fetch into a single DCQ snapshot for performance, and in the process switched the SOC source from Tesla's pre-scaled `soe.percentage` field (which already matches what the Tesla app shows) to a raw `nominalEnergyRemainingWh / nominalFullPackEnergyWh` ratio. The ratio gives the raw cell-level state and skips the 5%/95% scaling Tesla applies for user display — the Powerwall protects the bottom 5% of nominal capacity for cell health and won't discharge past it, so the operational range is 5–100%, not 0–100%. SOC is now scaled to match: at 24% raw the integration reports 20%, exactly like the Tesla app and Tesla cloud sensors. Anyone on v2.12.248 through v2.12.254 will see their `Home Battery Level` drop ~4% after upgrading — that's the corrected number, not new discharge.

Update available via HACS
