## What's Changed

**SAJ H2: Immediate battery response on restore_normal**
The `discharging_control` switch reflects the inverter's discharge pathway state — the firmware sets it OFF when `discharge_power_pct=0` and back ON when `discharge_power_pct=1100`. It cannot be forced ON while discharge is blocked. Previous restore_normal sent the master switch turn-on calls first (which had no effect while discharge_pct was still 0), then set discharge_pct=1100 as the 4th write — meaning the battery couldn't start discharging until several blocking Modbus calls had completed. Fixed: `discharge_power_pct=1100` is now written first, so the inverter opens the discharge pathway immediately and the battery starts serving home load with minimal delay.

Update available via HACS
