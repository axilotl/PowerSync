## What's Changed

**Flow Power Network Screen: Time Fields No Longer Block Saving**
The peak/off-peak time dropdowns on the Flow Power network & tariff options screen were rejecting submission with a "value must be one of..." error when the stored values didn't exactly match the available hour options (e.g. a previously saved half-hour value). A blank "—" option is now included in all four time selectors, and stored values that don't match are gracefully reset to their defaults.

**OCPP Charger Detection: Robust Entity Registry Lookup**
Charger ID extraction from OCPP integration entities was using a greedy regex that could incorrectly split entity names, and called `er.async_get()` inside a loop on every entity. Detection now uses a non-greedy regex anchored to the entity suffix, scans the entity registry once outside the loop, and adds debug logging to confirm what was found.

Update available via HACS
