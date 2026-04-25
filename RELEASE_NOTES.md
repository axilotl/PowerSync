## What's Changed

**Tesla Battery Health: corrected unit count for multi-pack Powerwall systems**
On Powerwall 3 systems with expansion packs, the Battery Health screen in the app was showing an inflated rated capacity (e.g. 54 kWh instead of 27 kWh for 1 Powerwall + 1 expansion) and a correspondingly deflated health percentage (e.g. 53% on a nearly-new system). The root cause: PW3 units each expose two BMS sub-modules in Tesla's Fleet API, so the module count from the BMS scan was double the actual number of physical Powerwalls. The calculation now cross-validates against Tesla's own `site_info` battery count, which correctly reports physical units, and uses that as the authoritative source when the two counts disagree.

Update available via HACS
