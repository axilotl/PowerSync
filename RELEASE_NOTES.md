<!-- release: v2.12.728 -->

## What's Changed

**Add hard caps for optimizer grid charging**
Smart Optimization now exposes advanced controls for a maximum grid charge price and a grid charge SOC cap. These settings let you keep forced grid top-up out of expensive import slots and stop grid charging once the forecast battery level reaches your chosen cap, while still allowing solar surplus to charge the battery above that cap.

**Apply grid-charge limits inside the solver**
The LP optimizer now carries a per-slot grid-charge permission mask through its cost model, period aggregation, forced-charge feasibility checks, and final action mapping. This keeps the new price and SOC caps consistent across normal optimization, Profit Max, export windows, and fallback schedules instead of only hiding the action at the UI layer.

**Group advanced optimizer controls in settings and docs**
The mobile/API settings payload, Home Assistant options flow, translations, and Smart Optimization wiki now describe the advanced optimizer controls together, including grid import/export limits, spread controls, No Idle, auto reserve, maximum grid charge price, and grid charge SOC cap.

**Retry incomplete Tesla restore operations**
Tesla restore-normal handling now keeps force-charge or force-discharge state active if a tariff, operation-mode, backup-reserve, export-rule, or grid-charging restore write fails. PowerSync schedules bounded retries instead of silently clearing the force state while the Powerwall may still need a successful restore.

Update available via HACS
