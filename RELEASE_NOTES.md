## What's Changed

**Solax Gen2/Gen3 Support**
The Solax controller now auto-detects which control model your inverter uses at startup — Gen4/Gen5/Gen6 (Manual Mode entities) or Gen2/Gen3 (Force Time Use entities) — and routes force charge, force discharge, backup reserve, and restore operations through the appropriate commands automatically. Gen2/Gen3 units previously failed with a missing-entity error; they now work without any configuration change. An optional entity prefix field has also been added to the setup flow for installations where the Solax Modbus integration creates entities under a custom naming group (e.g. `select.solax_modbus_charger_use_mode`).

**Optimizer Force Charge Windows**
A new `sensor.power_sync_optimization_force_charge_windows` entity shows all upcoming LP-planned grid charge windows — displayed as compact time ranges (e.g. `02:30-04:15`) with attributes including count, total duration, and per-window power and SOC. The Lovelace strategy dashboard automatically adds this card below the optimizer status tile when the entity exists.

**GoodWe EMS Power Limit Fix**
Fixed a crash when triggering force charge on GoodWe systems. The `number.goodwe_ems_power_limit` register only accepts values up to 32768 W (hardware limit); sending higher values (e.g. 50000 W from the app's force charge slider) caused a hard error. Values above 32768 W now clamp silently so force charge succeeds.

*Update available via HACS*
