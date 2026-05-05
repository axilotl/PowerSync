<!-- release: v2.12.297 -->

## What's Changed

**Tesla optimizer uses the refreshed TOU tariff**
For Tesla systems using a static TOU tariff such as GloBird, the LP optimizer now refreshes its cached tariff from Home Assistant's shared tariff schedule before building the price forecast. This fixes the case where the dashboard showed the correct tariff but the optimizer kept solving against a stale flat `31c import / 0c export` forecast, leaving no planned charges or discharges.

**Optimizer force modes are not replayed after restart**
PowerSync no longer reissues optimizer-owned force charge or force discharge commands after a Home Assistant restart or integration update. Stale optimizer force tariffs are cleared back to normal/self-consumption so the LP can recalculate from the current SOC, prices, and tariff instead of restoring an old force-discharge tariff.

Update available via HACS
