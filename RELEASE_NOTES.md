<!-- release: v2.12.698 -->

## What's Changed

**EV loadpoint source labels**
Solar-surplus owned EV charging sessions now keep the loadpoint source shown as solar even after the charger has consumed the available surplus. This fixes the EV panel showing Grid while Smart Schedule Solar Surplus is actively charging from solar generation.

**EV amp telemetry display**
The EV panel no longer shows a misleading 0 A value while a loadpoint is actively charging but the charger does not provide usable current telemetry. When observed amps are available, PowerSync now prefers that telemetry over a zero command-state value.

Update available via HACS
