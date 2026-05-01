## What's Changed

**Sigenergy export limit now respected during force discharge**
Force discharge (LP-driven exports and AEMO spike exports) previously bypassed the safety cap and could write the full battery rate — e.g. 14.4 kW on a system with a 5 kW DNSP cap — directly to the grid export limit register. The bypass was needed to escape a circular dependency in dynamic curtailment, but it also ignored the user-configured DNSP limit. Force discharge now clamps to the configured max export limit while still escaping the curtailment loop, so exports honour your grid agreement.

**Multi-vehicle EV charging uses per-vehicle charger config**
Previously, when the EV planner started a session it always fell back to the global generic-charger settings (max amps, voltage, phases, switch/amps/status entities), ignoring the per-vehicle charger config saved in the app. Now each vehicle's saved settings — including phases for amp-target calculation and the new `charger_status_entity` for plug detection — flow through to start/stop/amp-set commands. Generic-charger plug detection has also been aligned with the Tesla path so the planner correctly sees when a vehicle is connected.

**OCPP charger IDs no longer collide between loadpoints**
OCPP loadpoint commands now use a fully-qualified ID (preserving any `ocpp_` prefix already on the configured charger ID) instead of always wrapping it. This prevents two OCPP chargers configured against different vehicles from being treated as the same loadpoint.

**Legacy EV optimizer routes through shared charger actions**
The legacy LP-driven EV optimizer path now uses the same start/stop/set-amps helpers as the auto-schedule path, including session ownership claims. Behaviour is now consistent across both code paths — same retry handling, same ownership tracking, same charger-type dispatch.

**Phantom "_DEFAULT" EV no longer appears in mobile app**
The mobile app's energy flow could show a second phantom car labelled `_DEFAULT` at 0 W next to your real vehicle. The widget endpoint was emitting an entry for the internal `_default` placeholder key in the dynamic charging state when no display name was set, in addition to the real Tesla discovered separately. The widget now skips unnamed `_default` entries while preserving single-vehicle generic-charger setups where `_default` is legitimately the only key.

Update available via HACS
