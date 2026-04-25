## What's Changed

**Fix: Manual Start/Stop charging failed for Generic Charger (OCPP)**
When tapping Start or Stop on a vehicle connected via a Generic Charger (including OCPP via lbbrhzn/ocpp), the app returned "Vehicle is not plugged in" even when the status showed Preparing. The start/stop handlers were only checking Tesla Fleet/BLE plug state and had no path for Generic Charger — they'd always fail before reaching any switch command. Both Start and Stop now detect `vehicle_id = generic_ev` and route directly to the configured charger switch entity, with a plug check against the configured status sensor.

*Update available via HACS*
