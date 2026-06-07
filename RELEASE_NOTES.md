<!-- release: v2.12.607 -->

## What's Changed

**GoodWe entity-backed telemetry for LAN Kit systems**
GoodWe TCP / LAN Kit-20 setups can now use telemetry from the Home Assistant GoodWe integration's sensors when PowerSync detects a complete GoodWe telemetry entity surface. This avoids a second direct TCP/502 polling client during the normal 30-second telemetry refresh, reduces contention on LAN Kit systems, and still lets TCP setup complete when valid Home Assistant telemetry entities are present but direct TCP probing fails.

**GoodWe EMS restore limit handling**
GoodWe EMS entity control now restores the EMS power-limit entity from the inverter's rated power when available before falling back to the entity maximum. This prevents smaller inverters from being restored to the 32768W register ceiling after temporary force-mode control.

**Amber South Australia network detection**
Amber sites that report the network as `SA Power` now map to the `SA1` NEM region, matching the existing `SA Power Networks` handling and avoiding the periodic fallback warning.

Update available via HACS
