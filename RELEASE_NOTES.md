<!-- release: v2.12.632 -->

## What's Changed

**Tesla scheduled charging stop for second vehicles**
PowerSync now recognises Teslemetry charge switch aliases such as `switch.charge_2` when routing Tesla Fleet/Teslemetry stop commands to a specific VIN. This fixes scheduled charging and automation stop commands for second Tesla vehicles where the car was detected correctly but the matching charge switch was not found.

Update available via HACS
