## What's Changed

**Temperature-Aware Load Forecasting**
The historical load forecaster now optionally accounts for outdoor temperature when predicting consumption. After selecting a weather entity in settings, PowerSync fits a linear sensitivity coefficient (α) from your load history — typically 1–8% extra load per °C above the slot average for AC-heavy households. On a forecast 38°C afternoon vs a mild 22°C day, the optimizer will charge the battery harder on the hot day because it correctly anticipates higher home consumption. With no weather entity configured, behaviour is unchanged.

**Away Mode**
A new Away Mode switch tells PowerSync to ignore recent history when calculating the load forecast. When active, the estimator uses 28 days of history but skips the most recent 7 days — so a week of holiday-low usage doesn't deflate the forecast for the days after you return home. Toggle it on before leaving, off when you're back, and the next optimizer cycle refits using your normal pre-vacation pattern.

**Load Forecast Sensors**
Two new sensors — Load Forecast Today (Remaining) and Load Forecast Tomorrow — expose the optimizer's predicted home consumption as kWh entities in Home Assistant. Both include hourly breakdowns, peak kW, and flags for whether temperature adjustment and away mode were applied. The sensors appear automatically on the dashboard strategy and in the mobile app's optimization response when the LP optimizer is active.

Update available via HACS
