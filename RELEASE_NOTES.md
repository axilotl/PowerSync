<!-- release: v2.12.426 -->

## What's Changed

**Fixed Sungrow SH15T force-discharge power limits**
PowerSync now follows the upstream mkaiser Sungrow SH/T Modbus mapping for battery charge and discharge power limits. Sungrow force-discharge requests no longer write the rejected current-limit registers and instead update the SH/T max battery power registers before sending the forced discharge command, preventing SH15T systems from logging Modbus exception code 4 on register 13065 during optimiser export windows.

**Fixed Sungrow settings logging with missing reserve data**
The Sungrow settings endpoint now handles inverters that do not expose a backup reserve value without throwing a Home Assistant logging error.

Update available via HACS
