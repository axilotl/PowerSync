## What's Changed

**GoodWe: Force Charge and Force Discharge Now Actually Work**
When the GoodWe inverter was configured to connect via Modbus TCP (port 502 for data polling), force charge and force discharge commands were silently ignored — the inverter ACKs the Modbus write packets but never applies them to operational registers. Mode changes only take effect via GoodWe's proprietary UDP protocol on port 8899. The integration now opens a temporary UDP connection specifically for control commands when the data port is TCP, then verifies the mode change took effect by reading back the `work_mode` register. If UDP is unreachable, a clear error is logged explaining what needs to be fixed rather than silently failing.

*Update available via HACS*
