<!-- release: v2.12.564 -->

## What's Changed

**FoxESS curtailment now works across all inverter generations**
Zero-export curtailment relies on the inverter's export power limit entity, but the integration only recognised the H1/AIO name (`export_power_limit`). On H3/KH inverters — which expose it as `export_limit` — curtailment silently failed every cycle, so the battery and surplus solar kept exporting during zero-price windows instead of being held back. PowerSync now recognises all the foxess_modbus naming variants, so curtailment works automatically. When no export-limit entity is usable, the log now states the exact reason once (disabled entity to enable, or not exposed by your inverter) instead of repeating a generic error every few minutes.

**Smarter EV-aware battery optimisation**
The optimiser now refreshes your EV's charging forecast immediately before each planning solve, so battery decisions account for upcoming EV charging demand using fresh data. This is forecast-only — it updates the plan without sending any commands to your charger — giving more accurate home-battery scheduling when an EV is part of your setup.

**Energy history screen loads faster and more reliably**
The calendar/history view used by the mobile app now caches recent results and de-duplicates simultaneous identical requests, so repeated opens no longer hammer the Tesla API. If the underlying data is slow to fetch, it returns recent cached data (or a clean "still loading" response) instead of hanging, making the history screen feel snappier.

**Optimiser no longer momentarily freezes Home Assistant**
Building the load forecast scans your entire recorded load history, which was running on Home Assistant's main loop and could briefly stall the whole system on every optimisation cycle. That heavy work now runs on a background thread, and the history is scanned in a single pass instead of two — eliminating the periodic hitches on installations with large histories.

Update available via HACS
