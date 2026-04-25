## What's Changed

**OCPP charger shows "unavailable" in PowerSync app — fixed**
The PowerSync app was displaying OCPP chargers (via the lbbrhzn/ocpp HACS integration) as "unavailable" regardless of actual state. The root cause: `sensor.*_status` — the charge-point level sensor — commonly stays `unknown` in this integration, while `sensor.*_status_connector` (the connector-level sensor) updates reliably with the real state (`Available`, `Charging`, `Preparing`, etc.). PowerSync now falls back to `status_connector` when the primary status sensor is unknown, so the app correctly reflects charger state at all times.

**OCPP car plugged-in detection fixed for HACS lbbrhzn/ocpp integration**
When using the HACS lbbrhzn/ocpp integration (rather than PowerSync's built-in OCPP server), the EV auto-schedule planner was treating the car as never connected — causing solar surplus and price-level charging to never trigger even with a car plugged in. The planner now correctly checks `sensor.*_status_connector` entities from the `ocpp` platform, reporting the car as present during `Preparing`, `Charging`, `SuspendedEV`, and `SuspendedEVSE` states.

Update available via HACS
