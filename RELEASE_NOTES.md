<!-- release: v2.12.566 -->

## What's Changed

**FoxESS Cloud: full data and working controls on KH/K-series inverters**
FoxESS setups connected via Cloud API (no Modbus dongle) previously showed only battery percentage — solar, grid, load and battery power were all blank, and the online controls did nothing. This was because the integration read battery power from a variable that KH/K-series inverters (e.g. KH10) don't report. PowerSync now reads the model-specific power variables, so the complete energy flow populates correctly.

**FoxESS Cloud: mode and battery controls now apply with an active schedule**
Changing work mode, forcing charge/discharge, or setting a backup reserve silently failed whenever the inverter had a Mode Scheduler active (the FoxESS default). PowerSync now detects this, temporarily clears the blocking schedule, and retries — so the controls actually take effect.

**FoxESS Cloud: corrected export curtailment**
Export limiting was sending an incorrect value that the inverter interpreted as a near-zero export cap. Curtailment now sets the correct export ceiling in watts, and gracefully skips power-limit settings on models that don't support them instead of aborting.

Update available via HACS
