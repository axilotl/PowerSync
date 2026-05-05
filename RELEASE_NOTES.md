<!-- release: v2.12.290 -->

## What's Changed

**Treat Tesla BLE as vehicle telemetry, not a duplicate EV**
PowerSync now merges a single Tesla BLE bridge, such as an ESPHome `teslable` prefix, into the matching named Tesla vehicle when the same physical car is also visible through Fleet API or Teslemetry. The mobile dashboard and EV loadpoint status should now show the car name once, with Bluetooth-sourced SOC and plug state attached to that vehicle instead of rendering `Tesla BLE (...)` as a second EV.

**Keep ambiguous multi-car setups safe**
The merge only happens when there is exactly one named Tesla vehicle and one BLE bridge source. Multi-Tesla setups, standalone BLE-only vehicles, OCPP chargers, generic chargers, and Wall Connector-only telemetry remain separate unless PowerSync can identify a clear one-to-one match.

Update available via HACS
