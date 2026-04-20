## What's Changed

**Sungrow & GoodWe Modbus Connection Fix**
Fixed a setup failure affecting Sungrow SH-series, Sungrow SG-series, and GoodWe inverters where the Modbus port and slave ID were passed as floats rather than integers. This caused pymodbus to throw `'float' object has no attribute 'to_bytes'` on every register read, making the inverter appear unreachable during initial setup and at runtime. The error message incorrectly reported an internet connectivity problem rather than an inverter connection failure. All three inverter controllers now cast port and slave ID to `int` on construction — no configuration changes required.

Update available via HACS
