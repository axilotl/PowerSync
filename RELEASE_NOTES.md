## What's Changed

**Fix: FoxESS H3-Smart / Modbus "'float' object has no attribute 'to_bytes'"**
Resolves a bug that prevented FoxESS Modbus connections from working on fresh installs — the TCP connection succeeded but every register read failed with "'float' object has no attribute 'to_bytes'", and model auto-detection gave up with "FoxESS model detection failed — no registers responded". Home Assistant's NumberSelector stores the port, slave ID, and baud rate as floats (e.g. `502.0`, `247.0`), and pymodbus's wire-format serialiser calls `.to_bytes()` on the slave ID, which only works on ints. The FoxESS controller now coerces these three fields to integers at construction time, so existing installs with floats saved in the config entry recover on the next Home Assistant restart — no reconfigure needed.

Update available via HACS
