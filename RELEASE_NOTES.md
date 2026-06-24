<!-- release: v2.12.712 -->

## What's Changed

**Sungrow spread export fallback**
PowerSync now continues Sungrow spread export when the inverter rejects the optional discharge-rate limit register but still accepts the export-limit and forced-discharge commands. This helps SH-series setups that report Modbus exception code 4 on the max discharge register avoid dropping the entire export command.

**Sungrow restore handling**
When a Sungrow inverter has already shown that the discharge-rate limit register is not writable, PowerSync no longer treats restoring that optional limit as a failed restore step.

Update available via HACS
