<!-- release: v2.12.561 -->

## What's Changed

**Optimiser settings now apply instantly instead of a ~30s reload**
Changing an optimiser setting from the Home Assistant UI used to reload the whole integration — re-running every device and price connection — so the change took around 30 seconds to land. Those settings now apply directly to the running optimiser and re-optimise immediately, the same way the mobile app already does, so changes take effect in under a second with no reload. This covers backup reserve, battery capacity, charge/discharge/import limits, Profit Max, spread thresholds, cost function and EV integration. Structural changes that genuinely need a rebuild — switching the optimisation provider, enabling/disabling optimisation, the auto-apply-reserve toggle, monitoring mode, the Flow Power idle toggle and the Neovolt surplus mode — still do a full reload. The mobile app is unaffected.

Update available via HACS
