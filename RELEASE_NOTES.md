<!-- release: v2.12.688 -->

## What's Changed

**FoxESS curtailment now uses the live Modbus session**
FoxESS direct-Modbus solar curtailment now runs through the same coordinator-managed Modbus session used by force charge and force discharge commands. This prevents curtailment from bypassing the shared lock/connection context and failing silently when the controller is disconnected between polling cycles.

Update available via HACS
