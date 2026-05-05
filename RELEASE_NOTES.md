<!-- release: v2.12.298 -->

## What's Changed

**AEMO VPP uses the tariff schedule for normal pricing**
PowerSync now treats AEMO VPP as a retail tariff schedule with AEMO spike detection layered on top, rather than as a dynamic AEMO spot-price provider. This keeps normal LP pricing, EV planning, and tariff display on the configured tariff schedule while still allowing AEMO spike export events to trigger when the VPP threshold is reached.

**AEMO VPP restores saved Tesla tariffs correctly**
Tesla restore-normal handling no longer routes AEMO VPP through `sync_tou_schedule`, which intentionally skips VPP spike-only providers. When a force tariff ends, AEMO VPP systems now follow the saved-tariff restore path so the real Tesla tariff is restored instead of being left dependent on a skipped sync.

**Tesla Powerwall pack SOC is reconciled with aggregate BMS totals**
PowerSync now detects serial-less expansion packs that report a stale near-empty remaining-energy value while Tesla's aggregate BMS total proves the energy is still present. Those pack readings are reconciled from the aggregate total instead of showing a false 1-2% SOC beside the other balanced packs.

**Sigenergy force-charge respects requested charge power**
Sigenergy force-charge commands now apply the requested ESS max charge limit before entering charge mode. This keeps optimizer and manual force-charge setpoints from charging at the inverter's rated capacity when a lower target was requested.

Update available via HACS
