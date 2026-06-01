<!-- release: v2.12.525 -->

## What's Changed

**Powerwall local reserve readbacks now match the Tesla app scale**
When a Powerwall is paired locally, PowerSync now normalizes the local backup-reserve readback using the same hidden low-SOE reserve adjustment already used for overall SOC. A reserve set to 10% will no longer be read back as 5% through the local hardware path.

**Smart Optimization stops repeatedly reapplying unchanged Powerwall reserves**
The optimizer, Backup Reserve number entity, local snapshot, and mobile Powerwall settings view now all share the corrected local reserve interpretation. This prevents self-consumption mode from repeatedly re-sending the same reserve target when the hardware is already at the intended user-facing value.

Update available via HACS
