<!-- release: v2.12.474 -->

## What's Changed

**Flow Power account pricing now feeds Smart Optimization**
PowerSync now resolves Flow Power pricing through one shared path for the UI, tariff generation, cost tracking, and LP optimizer. When a Flow Power portal session is connected, the account TWAP, BPEA, and GST values feed import-price modelling before optimizer decisions are made, unless an explicit TWAP override is configured.

**Flow Power prices stay consistent across surfaces**
The current import-price sensor now reports the effective TWAP/BPEA/GST source, and the same calculation is used for generated tariff schedules and optimizer input prices. This prevents the dashboard from showing one Flow Power price while the optimizer plans against another.

Update available via HACS
