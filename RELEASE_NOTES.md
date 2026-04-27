## What's Changed

**SAJ H2 / HS2: Passive Mode Control Overhaul**
The SAJ H2 integration's force charge, force discharge, idle, and restore-normal behaviour has been corrected based on verification against the stanus74 integration source code and live device testing. The previous implementation used the passive charge/discharge *switch* entities, which do not manage AppMode — meaning the inverter could end up in an inconsistent state (passive register set but AppMode still on its TOU schedule) that caused erratic behaviour. All passive mode transitions now write directly to the `passive_charge_enable` and `app_mode` number entities, ensuring the inverter enters and exits passive mode cleanly every time.

**SAJ H2: Grid Charge Power Register Removed**
The `passive_grid_charge_power` register was being written during force charge operations, but testing by the stanus74 author confirmed it has no effect on actual charging behaviour. Writing it added unnecessary Modbus traffic and could mask the true charge rate. It is no longer written.

**SAJ H2: Grid Discharge Power Now Set Correctly**
During force discharge, `passive_grid_discharge_power` is now set to the same scaled value as the battery discharge target. This register *does* limit how much power the inverter can push to the grid, so leaving it unset was preventing full export rates in some installations.

**SAJ H2: Restore Normal Explicitly Sets All Registers**
`restore_normal` previously only turned off the two passive switches. It now explicitly zeros all passive power registers, writes `passive_enable=0`, turns off `charging_control` and `discharging_control`, and sets `AppMode=0` — matching the confirmed normal operating state observed on a live system.

**SAJ H2: Power Scale Fallback Changed to 1100**
When the inverter's rated capacity is unknown, the power fallback was 1000 (100%). The stanus74 register range is 0–1100, where 1100 is the integration's "no explicit limit — use inverter hardware max" sentinel. The fallback is now 1100, letting the inverter apply its own protection limits rather than artificially capping at 100%.

Update available via HACS
