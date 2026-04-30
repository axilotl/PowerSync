## What's Changed

**Battery Health: ghost-pack filter no longer drops real expansion packs**
The serialNumber-only ghost signal introduced in v2.12.244 was over-aggressive on some Powerwall 3 sites — specifically PW3+expansion installs whose firmware doesn't populate serialNumber for the expansion pack in the MSA components surface. The filter would treat the real expansion as a ghost candidate and drop it when systemStatus.nominalFullPackEnergyWh happened to match just the leader's energy (which made the cross-validation kept-sum check pass). One reported install dropped from a correct 2-pack count to 1.

The filter now requires **two signals together**: missing serialNumber AND near-zero remaining energy (< 500 Wh OR < 5% of full pack capacity). Real expansion packs always report remaining energy proportional to system SOC, so the new combined check distinguishes them from phantoms that sit at ~0 regardless of SOC. The cross-validation against systemStatus.nominalFullPackEnergyWh is unchanged — kept-pack sum must still match within 10% before any drop is applied. This makes the filter strictly more conservative; phantom slots that meet both criteria still get filtered, but real packs missing only one of the two ghost signatures are kept.

Sites that saw an under-counted battery total in v2.12.244–v2.12.245 will report the correct count again on the next BMS scan.

Update available via HACS
