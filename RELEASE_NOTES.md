## What's Changed

**SAJ battery State of Health is now exposed in PowerSync**
The SAJ controller now reads the `Bat1SOH` register (e.g. `sensor.saj_battery_1_soh`) and feeds it through the energy coordinator into the battery health sensor. Previously SAJ users saw `power_sync_battery_health = unknown` because the SoH wasn't mapped — even though stanus74's integration was already publishing it. The mapping wires through the same path the FoxESS/Sungrow/Sigenergy/GoodWe/Alpha bridges already use (`coordinator.data["battery_soh"]` → `BatteryHealthSensor._handle_coordinator_update`); SAJ was simply absent from the battery-system switch in the sensor wiring.

Update available via HACS
