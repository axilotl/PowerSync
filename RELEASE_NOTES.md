## What's Changed

**SAJ H2: Software safety guards prevent low-SOC lockout**
The SAJ H2 firmware shuts off its battery DC-DC converter when SOC reaches the on-grid discharge floor and does not auto-recover — only a power-cycle brings it back. Two upstream gaps make this trivial to trigger: (1) `passive_bat_charge_power_input` writes go to a register the inverter silently ignores while the converter is offline, and (2) the `discharge_depth` register can't be reliably written from the stanus74 integration, so the user-set min-SOC (e.g. 20%) doesn't reach the inverter — the hardware floor stays at 5% and the inverter happily discharges down to it.

PowerSync now refuses force commands when the inverter isn't engaged with the battery: `working_mode != 2` or R-phase inverter voltage < 50V. The user gets a clear error in the log instead of silent no-ops on dead Modbus writes. `force_discharge` additionally checks SOC against the configured backup_reserve (with a 1% buffer) and aborts before the BMS reaches the inverter's hardware lockout point. The user-facing min-SOC is now enforced in software because the hardware register is unwritable.

Update available via HACS
