## What's Changed

**SAJ H2: Fix restore_normal — battery now takes over home load immediately**
`passive_discharge_control` is the actual gate for battery discharge — confirmed by live testing: turning it ON with `discharge_power_pct=1100` causes the battery to switch from charging to discharging (~1730W) within one inverter poll cycle. `restore_normal` was incorrectly calling `turn_off(passive_discharge_control)`, keeping the battery in the same blocked state as force_charge. Fixed: `restore_normal` now turns `passive_discharge_control=ON` first, then sets `discharge_power_pct=1100`, so the battery starts serving home load on the first write rather than after a long delay. `charging_control` / `discharging_control` are read-back status indicators driven by inverter firmware — they cannot be set directly and all master switch calls have been removed.

Update available via HACS
