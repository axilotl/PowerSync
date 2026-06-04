<!-- release: v2.12.576 -->

## What's Changed

**Restore FoxESS H3 Smart force control**
PowerSync now falls back to the foxess_modbus `write_registers` service when the normal FoxESS work-mode entity no longer exposes Force Charge or Force Discharge. The fallback uses the H3 Smart/Pro remote-control registers through foxess_modbus, so PowerSync does not open a competing Modbus connection.

**Add FoxESS H3 Smart curtailment fallback**
For FoxESS H3 Smart/Pro-style profiles that do not expose an export power limit entity, PowerSync can now apply curtailment through the same upstream remote-control register path. The direct register fallback is model-gated so older H1, KH, and standard H3 profiles are not sent H3 Smart-specific commands.

**Restore remote control cleanly**
PowerSync now tracks when it has enabled FoxESS remote control directly and disables it again during restore, returning the inverter to Self Use where supported.

Update available via HACS
