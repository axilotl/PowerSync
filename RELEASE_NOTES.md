<!-- release: v2.12.411 -->

## What's Changed

**Fix Sungrow SH export power commands**
Sungrow SH-series forced charge and discharge commands now pass the requested power all the way through to the inverter's forced-power register. This prevents SH20T and other higher-power Sungrow systems from being capped at the old 5 kW fallback when PowerSync or Smart Optimization requests a larger export rate.

**Add Sungrow command regression coverage**
Added focused tests for the Sungrow coordinator and Modbus controller paths so future changes must preserve the requested charge/discharge wattage instead of only updating the rate-limit register.

Update available via HACS
