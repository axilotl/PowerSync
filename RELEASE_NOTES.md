<!-- release: v2.12.719 -->

## What's Changed

**Flow Power current price smoothing**
PowerSync now keeps Flow Power current import pricing on the canonical 30-minute billing tariff when publishing the standard current price schedule. The live 5-minute KWatch dispatch value is no longer injected into the active 30-minute PEA schedule, which prevents the current import price sensor from briefly spiking or dipping in the final minutes before `:00` and `:30` boundaries.

Update available via HACS
