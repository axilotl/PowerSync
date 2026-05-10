<!-- release: v2.12.376 -->

## What's Changed

**Tesla self-consumption no longer raises backup reserve above current SOC**
PowerSync now caps Tesla backup-reserve writes during self-consumption so the Powerwall is not asked to charge from the grid up to the optimizer discharge floor when the battery is already below that floor. If the Powerwall is at 11% and the optimizer floor is 25%, PowerSync will preserve or lower toward the saved reserve instead of writing 25% and triggering grid charging.

Update available via HACS
