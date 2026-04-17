## What's Changed

**Sigenergy force discharge: spurious Modbus error gone**
Force discharge cycles were logging an error and warning every run — `Modbus write error at register 40001: ExceptionResponse(... exception_code=3)` followed by `Failed to set active power target ..., falling back to export limit only`. The active power target register is only writable in PCS Remote mode, but the controller has already switched to DISCHARGE_ESS mode one step earlier, so the inverter correctly rejected the write. The redundant write is now removed; the grid export limit (which is what actually controls discharge rate in this mode) is still set, so discharge behaviour is unchanged — only the noise disappears.

Update available via HACS
