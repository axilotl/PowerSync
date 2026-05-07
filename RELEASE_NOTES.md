<!-- release: v2.12.317 -->

## What's Changed

**SAJ H2 force modes clear stale switch controls**
Force charge and force discharge now turn off any stale SAJ passive/manual charge or discharge switches before handing control to TOU slot 7. This keeps the Home Assistant switch surface aligned after moving force charge away from passive mode, while preserving the slot-7 Modbus schedule path used by the optimizer.

Update available via HACS
