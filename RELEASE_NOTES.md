<!-- release: v2.12.540 -->

## What's Changed

**Cleaner Sungrow AC inverter restore enforcement**
PowerSync still sends the periodic Sungrow AC inverter restore command used to keep the inverter awake and clear any stuck curtailment state, but recurring restores no longer force an immediate Modbus readback. This keeps the existing keep-alive behavior while reducing confusing `pymodbus` transaction and register-read noise in Home Assistant logs.

**Smarter optimizer IDLE hold reporting and restore handling**
Temporary IDLE hold reserve levels are now tracked separately from the optimizer reserve floor, exposed on optimizer sensors, and shown as an `IDLE Hold` line on the dashboard. Exiting IDLE also restores the user's pre-IDLE hardware reserve more reliably, including FoxESS-style work mode restores.

**Auto reserve option changes apply immediately**
Changing the optimizer auto reserve toggle in options now updates the live optimization coordinator before Home Assistant reloads the config entry. This prevents the UI setting from lagging behind the running optimizer state.

**Recent load regime adjustment**
The load forecaster now detects sustained recent load shifts, such as a cold-weather step change, and blends that signal into the forecast without reacting to short spikes. This should improve planning when the last couple of days no longer match the older history pattern.

Update available via HACS
