## What's Changed

**Optimizer no longer uses wholesale prices on a static-TOU plan**
Two correctness gaps when users either chose a static-TOU provider (Globird, AEMO VPP, "other / custom TOU", Tesla-only TOU, NZ retailers) or switched providers after starting on Flow Power. The Flow Power → AEMO price source check fired purely on the persisted `flow_power_price_source` option without verifying that Flow Power was still the configured provider, so a user who switched to e.g. Amber would still spin up the AEMO coordinator at startup and feed AEMO data into paths that shouldn't see it. Separately, the optimizer's price-forecast routine could fall through to a leftover `AEMOPriceCoordinator` for static-TOU users if the TOU tariff schedule wasn't yet cached — silently optimizing on stale wholesale prices for someone who explicitly picked a fixed-rate plan.

The fix: the AEMO setup in `__init__.py` now requires `electricity_provider == "flow_power"` before activating; the `OptimizationCoordinator` now exits the dynamic-pricing listener path early for static-TOU providers (unsubscribing any pre-existing listener) and explicitly returns no prices when the TOU schedule isn't ready yet rather than silently using whatever happens to be in the price coordinator. End result: static-TOU users always see their fixed rates (or no rates at all if the schedule hasn't loaded), never a wholesale figure they didn't ask for.

A new regression test file (`tests/test_optimization_price_source.py`) covers all four code paths: static-TOU with cached tariff, static-TOU with no cached tariff, the dynamic-listener gate, and an AST spot-check of the Flow Power gate.

Update available via HACS
