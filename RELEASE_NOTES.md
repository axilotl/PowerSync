## What's Changed

**SAJ grid power now reads the whole-house CT meter first**
The SAJ controller's `grid_power` slot tried `gridPower` (the inverter's own grid-leg measurement) before `CT_GridPowerWatt` (the whole-house meter). On systems with AC-coupled solar from a separate inverter, those two registers diverge — the inverter's grid leg only sees its own contribution, while the CT meter sees the actual house-to-grid flow including everything from the AC-coupled inverter. The matching `solar_power` slot already preferred the CT (`CT_PVPowerWatt`); grid is now aligned to the same principle. On systems where both readings agree (no AC-coupled generation) the change is a no-op; on hybrid setups it removes a class of silent under-reporting where PowerSync would think a smaller amount was flowing to/from the grid than actually was.

Update available via HACS
