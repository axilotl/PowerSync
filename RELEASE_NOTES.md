## What's Changed

**Generic EV Charger: Fix "Vehicle is not plugged in" false error**
When using the HACS lbbrhzn/ocpp integration, the charger-level status sensor (e.g. `sensor.ocpp_status`) can report "Available" even when a car is physically connected — the more accurate signal is the connector-level entity (e.g. `sensor.*_status_connector`) which correctly shows "Preparing". The manual Start button and plugged-in detection now fall back to checking connector-level entities before rejecting, so "Preparing" on the connector is correctly treated as plugged in.

Update available via HACS
