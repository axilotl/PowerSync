## What's Changed

**Per-vehicle EV charger configuration**
The EV planner now reads each vehicle's own charger settings — type, switch entity, amps entity, voltage, phases, status entity, and OCPP id — instead of falling back to a single global config. Multi-vehicle households can now mix charger backends (e.g. one Tesla + one generic OCPP wallbox) and have each vehicle's amp targets, plug detection, and start/stop commands resolved against its own physical charger. Voltage and phase counts are also taken from the per-vehicle config when computing target amps, so 3-phase EVSEs no longer get capped at single-phase math.

**Generic charger plug detection no longer blocks charging**
When a generic charger has no status entity configured — or the status entity reports an unknown state — the planner now treats the EV as ready instead of bailing out. Previously, missing or non-standard status sensors silently prevented charging from ever starting on generic backends.

**Price-level charging works for generic and multi-vehicle setups**
Cheap-price opportunity charging now routes through the correct loadpoint id (`generic_ev`, `zaptec_standalone`, or per-vehicle VIN) rather than always assuming a Tesla. Households running an OCPP or generic charger as their only EV source will now actually start/stop on price triggers.

**OCPP command routing fixes**
Resolved a double-prefix bug where an OCPP charger id of `ocpp_evse_1` was being turned into `ocpp_ocpp_evse_1`, breaking switch lookups. The mobile/manual command path also now recognizes any `ocpp_*` loadpoint id directly, so app-issued start/stop commands reach the right charger.

**Unified legacy EV optimizer with shared charger actions**
The legacy `EVCoordinator` (used by the original solar-surplus optimizer for native HA switches, OCPP, and Zaptec) now goes through the same shared action layer as the new dynamic chargers. This eliminates two divergent codepaths, so amp setting, ownership claims, and failure reasons behave consistently across both optimizer generations.

Update available via HACS
