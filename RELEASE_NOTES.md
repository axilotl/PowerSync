## What's Changed

**SAJ H2: Fix IDLE mode — discharge_switch must be ON for discharge_pct=0 to lock the battery**
`set_idle()` in 2.12.187 set `passive_battery_discharge_power = 0` but left `passive_discharge_control` OFF. Live testing confirmed this register only locks the battery when the passive discharge switch is active — in normal self-consumption mode (discharge_switch OFF), the register is ignored and the battery continues discharging freely. Fixed: `set_idle()` now mirrors `force_discharge` at 0% rate, turning on `passive_discharge_control` after setting `passive_enable = 2`. `restore_normal()` correctly exits this state.

Update available via HACS
