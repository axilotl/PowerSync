<!-- release: v2.12.448 -->

## What's Changed

**Faster LP optimizer solves**
PowerSync now builds the internal LP schedule with a HAEO-style variable timeline: near-term control stays at 5-minute precision, while later horizon periods are safely aggregated and split again around export rules, charge blocks, price changes, deadlines, and solar/load transitions. This cuts the normal 48-hour optimization model from hundreds of fixed slots to roughly the low hundreds without changing the 5-minute schedule published to Home Assistant.

**Sparse energy-state LP model**
The optimizer now uses explicit battery energy boundary variables and sparse SciPy HiGHS matrices instead of dense cumulative SOC rows. This keeps reserve floors, export guards, no-grid-charge behavior, Flow/Happy Hour windows, and below-reserve recovery semantics intact while materially reducing formulation and solve overhead.

**Optimizer performance diagnostics**
LP runs now publish solver stats through the existing Current Action sensor attributes, including backend, formulation time, solver time, variable count, constraint count, nonzero count, period count, and fallback reason when applicable. A new opt-in benchmark script covers flat, volatile, export, no-grid-charge, and reserve recovery scenarios so future solver changes can be measured before release.

Update available via HACS
