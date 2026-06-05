<!-- release: v2.12.593 -->

## What's Changed

**Home Load history no longer disappears after invalid power spikes**
PowerSync now prevents impossible negative Home Load readings from being published or drawn in the dashboard history chart. This keeps the 24-hour Energy card readable even if an inverter briefly reports an inconsistent set of live power values during battery mode transitions.

**FoxESS calculated load is steadier during mode changes**
FoxESS H3-Pro and H3-Smart direct-Modbus systems now keep the last valid calculated Home Load when a transient register mix would otherwise produce an invalid value. This prevents bad load points from polluting recorder history while preserving normal load tracking.

Update available via HACS
