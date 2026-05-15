<!-- release: v2.12.409 -->

## What's Changed

**GoodWe EMS restore recovery**
GoodWe entity-mode restores now also reset the companion inverter operation-mode select back to General when that entity is available. This closes a restore gap where PowerSync cleared the EMS power limit and selected EMS Auto, but the inverter could remain in an Eco/exporting operation state after a force charge ended.

**GoodWe restore diagnostics**
PowerSync now logs the optional inverter operation-mode restore separately, making it easier to confirm whether Home Assistant exposed `select.<prefix>_inverter_operation_mode` and whether the General-mode reset was accepted.

Update available via HACS
