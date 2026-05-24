<!-- release: v2.12.465 -->

## What's Changed

**Sigenergy EVDC V2X power is modeled separately from home load**
PowerSync now reads configured Sigenergy EVDC charger telemetry during the Sigenergy energy update, normalizes discharge as negative EV power, and excludes that signed EVDC branch from the site load calculation. This prevents DC-side vehicle charging from being counted as household demand and lets V2X discharge appear as an EV supply branch instead of a battery or load artifact.

**EV status and dashboard flows understand EV discharge**
The EV status sensor and energy-flow dashboard now preserve signed EV power, expose whether a Sigenergy EVDC charger is discharging, and render vehicle-to-home or vehicle-to-grid flow as green supply. The dashboard cache version was bumped so Home Assistant clients fetch the updated flow logic.

**Home Assistant Smart Optimization settings include EV integration**
The Smart Optimization setup and options pages now expose the same EV Charging Integration toggle already available in the mobile app. The value is saved through the existing optimizer option key and is also honored when it was chosen during first-time setup before any options save exists.

Update available via HACS
