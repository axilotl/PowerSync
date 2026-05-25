<!-- release: v2.12.469 -->

## What's Changed

**FoxESS entity bridge startup retry**
PowerSync now keeps the FoxESS entity bridge coordinator active when Home Assistant starts before `foxess_modbus` has finished restoring its entities. This prevents FoxESS sensors from staying unavailable after a restart and lets the bridge recover automatically instead of requiring a manual PowerSync reload.

Update available via HACS
