## What's Changed

**SAJ H2: Faster restore_normal — battery takes over load immediately**
`restore_normal` was enabling the master discharge switch last, after 5+ blocking service calls, so the battery couldn't start discharging until all passive register writes had completed. The master switches (`discharging_control` / `charging_control`) are now turned on first so the inverter immediately picks up the home load from the battery while the passive register cleanup happens in the background. Also sets `passive_battery_charge_power` to 1100 (was 0) so the battery can charge from solar at full rate in self-consumption mode.

Update available via HACS
