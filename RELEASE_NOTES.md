## What's Changed

**SAJ H2/HS2: Fixed battery data not appearing**
The SAJ H2 integration was failing to discover any entities because it was searching for unique ID suffixes using camelCase names (`batteryPower`, `Bat1SOC`) while the stanus74 integration actually uses snake_case (`battery_power`, `battery_1_soc`). This meant battery level, solar, grid, and load power all showed as unavailable from the moment the integration loaded. All suffix strings have been corrected to match what stanus74 actually creates.

**SAJ H2/HS2: Correct battery and grid power sign conventions**
Battery and grid power values from the SAJ H2 are unsigned absolute values — the inverter reports separate `direction_battery` and `direction_grid` sensors (1=charging/import, 2=discharging/export) to indicate direction. PowerSync now reads these direction sensors and applies the correct sign, so charge/discharge and import/export show correctly in the dashboard and feed the optimizer accurately.

**SAJ H2/HS2: Fixed force charge/discharge control**
The control entity names were wrong (`passive_battery_charge_power_2`, `passive_charge_enable_2`) — the actual number and switch entities created by stanus74 are `passive_battery_charge_power_input` and `passive_charge_control`. Power is now set in watts directly rather than through an incorrect 0-1000 internal scale.

**SAJ H2/HS2: Improved startup diagnostics**
Connect validation no longer fails if the passive-mode control entities are missing — these are optional and the integration will still work for monitoring. The full entity map is logged at INFO on startup to make misconfigured setups easy to diagnose.

Update available via HACS
