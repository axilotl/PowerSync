## What's Changed

**Solax Hybrid Battery System Support**
Solax Hybrid inverters (X1/X3, Gen4/Gen5/Gen6 and AC Retro-Fit) can now be used as a PowerSync battery system. PowerSync bridges through the [wills106/homeassistant-solax-modbus](https://github.com/wills106/homeassistant-solax-modbus) HACS integration — no direct Modbus connection is opened, so your existing solax_modbus setup keeps running untouched. Install solax_modbus from HACS first, then add Solax Hybrid as your battery system in the PowerSync config flow.

**Force Charge / Discharge & LP Optimizer Integration**
The LP optimizer can now schedule Solax charge and discharge windows using Manual Mode on the inverter. Force charge writes the target current to `battery_charge_max_current`, sets `charger_use_mode` to Manual Mode, and sets `manual_mode` to Force Charge. A Home Assistant timer automatically restores Self Use mode when the window expires. Backup reserve, operation mode (Self Use / Feed-in Priority / Back Up / Smart Schedule), and grid export limit are all controllable through the standard PowerSync services.

**Missing-Entity Validation at Setup**
If the solax_modbus integration isn't installed or the entity prefix doesn't match, the config flow lists the specific missing entity IDs in the error message rather than showing a generic failure — making it straightforward to identify which entities need to be present before setup can complete.

Update available via HACS
