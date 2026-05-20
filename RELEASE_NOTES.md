<!-- release: v2.12.447 -->

## What's Changed

**Sigenergy Smart Schedule charger start fix**
Fixes Smart Schedule starts for Sigenergy EVAC/EVDC chargers when older or blank charger settings were saved before the dedicated Sigenergy backend was selected. Those sessions could decide correctly that the charger should start, then fall through to the Tesla-only charge path and fail with missing Tesla charger entities. Smart Schedule now resolves legacy charger settings to the configured Sigenergy backend and carries the Modbus charger details through both start and charge-rate update paths.

Update available via HACS
