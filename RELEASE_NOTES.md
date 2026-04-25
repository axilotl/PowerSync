## What's Changed

**Fix: Smart charging automations never triggered for Generic Charger (OCPP)**
Solar surplus charging, price-level charging, and scheduled charging evaluate which chargers are present by checking Tesla vehicles first, then Zaptec, then the built-in OCPP server — but Generic Charger was missing from this chain entirely. A site with only a Generic Charger (e.g. lbbrhzn/ocpp) would silently produce no charging decisions at all. The evaluator now includes Generic Charger as a fallback after OCPP, using the same plug-detection and start/stop logic already in place for other charger types.

*Update available via HACS*
