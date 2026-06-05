<!-- release: v2.12.596 -->

## What's Changed

**Optimizer reserve protection for Profit Max exports**
Profit Max and Spread Export now keep export planning above the configured optimiser reserve instead of spreading or bridging export slots down toward the hardware reserve. Auto-Apply reserve also snapshots the current visible reserve when enabled and keeps the manual restore reserve in sync when the backup reserve is changed while Auto-Apply is off.

**Optimizer horizon setting now applies and persists**
The optimiser settings API now persists `horizon_hours`, restores it on startup, and passes it through to the LP optimiser so accepted horizon changes actually affect the forecast window used for scheduling.

**Force discharge cleanup after accepted Tesla tariff uploads**
Tesla force-discharge now tracks when a tariff upload was accepted even if the readback confirmation later fails, arms the restore cleanup anyway, and permits that cleanup to release an active force tariff in monitoring mode.

**Solar forecast provider selection**
Weather and Solcast settings now include a solar forecast provider preference for Solcast or Open-Meteo. Optimisation, automations, and EV surplus planning use the configured provider first and fall back to the other supported source when no usable forecast is available, while preserving the legacy Solcast automation key.

**Dashboard optimisation plan caching**
The optimisation plan card now shares a short browser-side cache and in-flight request promise so frequent dashboard updates do not hammer the optimisation API.

**Inverter and cloud API fixes**
FoxESS Scheduler V3 writes no longer inject default import/export/PV/reactive limits when those limits were omitted, preserving device-side settings. SolarEdge entity auto-mapping now avoids treating battery or meter DC power sensors as solar production.

Update available via HACS
