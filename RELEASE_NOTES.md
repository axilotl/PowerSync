## What's Changed

**GoodWe: Force Charge/Discharge Now Works via Modbus TCP Gateway (EMS Mode)**
Many GoodWe hybrid inverters are only accessible via a Modbus TCP gateway rather than direct WiFi — in this setup, writes to operation mode registers are silently ignored by the inverter, making force charge and force discharge effectively broken. This release adds an "EMS Entity Prefix" option (in PowerSync's GoodWe Connection Settings, typically set to `goodwe`) that routes force charge/discharge through the community GoodWe HA integration's EMS mode entities (`select.<prefix>_ems_mode` and `number.<prefix>_ems_power_limit`). These registers accept Modbus TCP writes and immediately take effect — confirmed live with sustained 3kW grid export. IDLE and self-consumption modes correctly restore `ems_mode` to `auto`. Requires the [GoodWe HA integration](https://github.com/mletenay/home-assistant-goodwe-inverter) to be installed alongside PowerSync.

**GoodWe: Force Mode No Longer Stalls for 10 Seconds When UDP Is Blocked**
Previously, when the GoodWe inverter's UDP port 8899 was unreachable (e.g. behind a gateway), every force charge/discharge call would time out after 10 seconds before falling back to TCP. A 5-minute failure cache now skips the connection attempt after the first timeout, so subsequent calls return immediately with a warning instead of stalling the coordinator.

Update available via HACS
