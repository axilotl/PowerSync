## What's Changed

**Fix: EV smart schedule never triggered when using a binary sensor for plug-in detection**
Users who configured a `binary_sensor.*` entity (such as `binary_sensor.tesla_wall_connector_vehicle_connected`) as their generic charger status entity would find the auto-schedule silently skipping their vehicle every cycle — even when the car was actually plugged in. The detection code was checking for OCPP-style states (`charging`, `preparing`, etc.) which binary sensors never produce; they return `on`/`off`. The scheduler now correctly treats `on` as plugged-in for binary sensor entities, while OCPP and other charger status sensors continue to use their existing state list.

**Fix: Solax prefix discovery no longer matches EV charger integrations**
The Solax config flow's automatic prefix detection was matching any integration that had a `charger_use_mode` select entity — including Solax EV charger integrations, which share that entity name but are not hybrid inverters. The discovery now requires both `charger_use_mode` and `battery_capacity` to be present for the same prefix, ensuring only the wills106 Solax Hybrid inverter integration is matched.

Update available via HACS
