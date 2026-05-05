<!-- release: v2.12.292 -->

## What's Changed

**EV dashboard duplicate vehicle fix**
PowerSync now collapses duplicate Tesla Fleet/Teslemetry records for the same VIN before merging Tesla BLE bridge telemetry. This prevents the mobile app and EV loadpoint API from showing one physical car as both the named Tesla vehicle and a separate Tesla BLE vehicle.

**Cleaner EV counts for mixed Fleet and BLE setups**
Vehicle status, automation vehicle pickers, and mobile vehicle lists now dedupe Tesla devices by VIN when multiple HA Tesla integrations expose the same car. BLE data still supplements the matched vehicle, including live SOC and plug state, without creating a second loadpoint.

Update available via HACS
