## What's Changed

**SAJ H2: Fix force_charge / set_idle — use master charge/discharge switches**
`switch.saj_discharging_control` and `switch.saj_charging_control` are the inverter's actual battery gates — `passive_discharge_control` does not override them. Force charge was turning off `passive_discharge_control` but leaving `discharging_control` ON, so the battery kept discharging at ~1800W in self-consumption mode regardless. Fixed: force_charge now turns off `discharging_control` (the master switch), preventing discharge so the grid/solar covers home load and charges the battery. Force discharge and set_idle updated to use the same master switches consistently. Restore normal re-enables both.

Update available via HACS
