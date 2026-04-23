## What's Changed

**Battery Health: Ghost Expansion Packs No Longer Shown**
The Tesla Fleet API sometimes returns BMS entries for expansion pack *slots* that are registered in the site configuration but not physically installed. These phantom entries — with empty serial numbers and identical stale energy readings (14.47 kWh rated / 0.20 kWh remaining) — were showing up as Expansion 1, 2, 3 in the Battery Health screen, with incorrect stats like 26.6% health and 54 kWh rated capacity. The integration now cross-validates individual BMS pack data against the system-level energy total reported by Tesla: if the expansion entries don't contribute to the system aggregate, they're dropped. Single-Powerwall users will now see correct results — one Main Unit, 13.5 kWh rated, and accurate health. Systems with real expansion packs installed are unaffected.

Update available via HACS
