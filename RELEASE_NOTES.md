## What's Changed

**SAJ H2: Fix entity discovery — sensor keys corrected to match stanus74 unique_id format**
The stanus74 `saj_h2_modbus` integration uses camelCase unique_id keys (`batteryPower`, `Bat1SOC`, `gridPower`, `pvPower`, `TotalLoadPower`, `directionBattery`) but the PowerSync bridge was searching for snake_case suffixes. None of the power sensor slots were mapping to real entities, so battery level, power, grid, solar, and home load all read 0.0. All key mappings are now corrected to match the actual stanus74 unique_id format.

**SAJ H2: Fix direction sensor convention — 1=discharging, -1=charging**
The bridge was interpreting the SAJ direction sensors backwards: value `1` is discharging/export, value `-1` is charging/import. The previous code had this inverted, causing battery power and grid power signs to be wrong (e.g. a discharging battery would show as negative/charging in PowerSync).

**SAJ H2: Prefer fast-poll sensors over slow-poll for fresher readings**
The stanus74 integration creates fast-poll variants of power sensors (e.g. `sensor.saj_fast_battery_power`) that update more frequently than the standard counterparts. PowerSync now picks the fast variant first for all power and direction slots, giving the house scene and optimizer more responsive readings.

**SAJ H2: Fix force charge/discharge control entity discovery**
The passive charge/discharge number entities are named `passive_battery_charge_power` (not `passive_bat_charge_power` as previously coded). The incorrect suffix meant force charge and force discharge commands could never find the control entities and would silently fail.

Update available via HACS
