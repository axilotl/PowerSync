<!-- release: v2.12.691 -->

## What's Changed

**Editable battery and control method settings**
Existing PowerSync entries can now change the selected battery or inverter control method from the options flow without deleting and re-adding the integration. This includes Custom external controller, Anker Solix, AlphaESS, and the other supported systems, with connection saves reloading the entry so the runtime coordinator matches the selected method.

**Charge By Time for Smart Optimization**
Smart Optimization now separates Charge By Time from Profit Max. Profit Max can focus on profitable export behavior, while Charge By Time handles reaching a configured battery SOC by a target time. Existing Profit Max fill-by settings are migrated into the new Charge By Time settings, and the mobile/API compatibility aliases remain available.

**Sungrow load fallback**
Sungrow SH telemetry now derives household load from the energy balance when firmware reports a zero or missing load register while PV, grid, and battery values still indicate real load.

**Documentation and translations**
The README, docs site, Smart Optimization wiki page, options-flow labels, and English translations were updated for the new controls and connection option pages.

Update available via HACS
