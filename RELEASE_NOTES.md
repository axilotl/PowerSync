<!-- release: v2.12.609 -->

## What's Changed

**Sigenergy force discharge chooses the right Remote EMS mode**
Sigenergy force discharge now chooses between PV-first and ESS-first dispatch from live solar output and the effective export target. Systems where PV-first does not pull from the battery can use ESS-first when the requested export needs storage contribution, while systems that rely on PV-first to avoid suppressing solar keep that path when solar can cover the target. Configured DNSP export caps are still honoured before the mode decision.

**Enphase DPEL relay payload compatibility**
Enphase DPEL export limiting now sends the structured neutral relay configuration expected by newer Australian IQ Gateway firmware, while still retrying the older boolean relay payloads for gateways that accept those formats. This should reduce 400 responses when applying zero-export or load-following curtailment on D8.3.x firmware.

Update available via HACS
