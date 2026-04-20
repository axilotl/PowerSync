## What's Changed

**Flow Power Setup: Simplified Tariff Configuration**
The initial Flow Power setup no longer shows an overwhelming dropdown of 88 network tariffs from every distributor in Australia. Instead, the flow is split into two focused steps: select your NEM region and base rate first, then pick from only the distributors that serve that region on a separate screen. The default region is now NSW1 (previously QLD1). Existing users are unaffected — this only improves the setup experience.

**Flow Power Options: Removed Duplicate Tariff Selectors**
The Flow Power options screen previously showed three overlapping tariff-related fields at once (a combined legacy dropdown, plus separate network and tariff code pickers). These have been consolidated — the main options screen now shows only region, price source, base rate, PEA toggle, and sync toggle. Network distributor, tariff code, TWAP override, and Amber markup have been moved to the dedicated "Network & Tariff" screen on the next step.

**Monitoring Mode: Price Sensors Now Update Correctly**
When Monitoring Mode was enabled, the entire TOU sync function returned early, preventing `current_import_price` and `current_export_price` sensors from ever getting their values. The monitoring mode check has been moved to just before the battery API calls — the tariff schedule is now always stored for display purposes, and only the actual battery commands (Tesla, Sigenergy, FoxESS) are blocked. Users running in monitoring mode will now see live price sensors.

**FoxESS Force Discharge: Precise Grid Export Target**
Force discharge on FoxESS H3-Pro and H3-Smart inverters now uses Grid target mode (`REMOTE_CONTROL_GRID`) instead of AC target mode. This instructs the inverter to hold total grid feed-in at the requested power level, automatically reducing battery contribution when PV generation is active — so the actual export figure is accurate for tariff events (e.g. GloBird bonus export). Force charge continues to use AC target mode, which commands battery power directly and is unaffected by concurrent EV or house loads.

**Load Forecast: kW/W Unit Mismatch Fixed**
The load forecast sensor was dividing by 1000 twice — the internal forecast array already stores values in kW, but the sensor code was treating them as watts and converting again. This caused forecasted load figures to appear 1000× too small on the app's forecast charts. Values are now correct.

**Force Charge/Discharge Duration Fix (Web App)**
When force charge or discharge commands were triggered from the web app, the duration was ignored and the default (30 or 60 minutes) was used instead. The web app sends duration under the key `"minutes"`, while the mobile app uses `"duration_minutes"` and HA automations use `"duration"` — the handler now checks all three.

**Modbus Connection Fix for GoodWe and Sungrow**
Port and slave ID values from the config entry were being passed as strings to the Modbus client constructors (GoodWe, Sungrow SG, Sungrow SH), which could cause connection failures on some setups where the config was stored as string types. These are now explicitly cast to `int` at construction time.

Update available via HACS
