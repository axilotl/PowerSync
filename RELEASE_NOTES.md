<!-- release: v2.12.490 -->

## What's Changed

**Full SolarEdge battery control**
SolarEdge Home Battery installs can now use PowerSync's normal force charge, force discharge, restore normal, backup reserve, Hold SOC, Smart Optimization, AEMO spike, Saving Sessions, and mobile control paths when the SolarEdge Home Assistant storage-control entities are exposed. Telemetry-only SolarEdge setups still load for live flow and sensors, but dispatch now fails with clear missing-entity diagnostics instead of silently behaving like a read-only integration.

**SolarEdge setup and docs now match the new control surface**
The SolarEdge setup copy, README, and wiki now describe the HA entity bridge for telemetry and battery dispatch, plus the existing Modbus/entity fallback path for inverter curtailment. Troubleshooting now calls out the writable storage-control entities needed for force charge/discharge and reserve control.

**Scheduled EV charging leaves away vehicles alone**
Scheduled charging no longer stops an externally-started charge session just because the local schedule is inactive when the vehicle is away from home. PowerSync still manages configured home chargers and vehicles confirmed to be at home, while avoiding remote interruptions for away sessions.

Update available via HACS
