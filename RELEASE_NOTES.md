## What's Changed

**New Battery Brand: ESY Sunhome (HM Series)**
ESY Sunhome batteries are now fully supported. PowerSync integrates via the [ESY Sunhome integration](https://github.com/branko-lazarevic/esysunhome) (available on HACS) as a companion — you install that integration separately to pair your device, and PowerSync bridges through it for telemetry and control. No direct cloud credentials are required in PowerSync itself.

**LP Optimizer + AEMO Spike Export Support for ESY Sunhome**
The built-in LP optimizer runs full charge/discharge scheduling for ESY Sunhome batteries. Optimizer commands map to ESY's native operating modes: Emergency Mode for grid charging, Electricity Sell Mode for export, and Regular Mode for self-consumption. AEMO price spike export and Saving Sessions are also enabled. Note that ESY Sunhome uses mode-only control — charge/discharge power levels are managed by the battery firmware, not set explicitly.

**Live Sensors: Inverter Temperature, Battery Status, State of Health**
Three ESY-specific sensors are registered alongside standard battery/grid/solar telemetry: inverter temperature (°C), battery status (text from firmware), and battery state of health (%). All standard Power Flow, Energy Charts, and LP Forecast dashboard sections work automatically.

**Setup: Graceful Handling When ESY Sunhome Is Not Installed**
If the ESY Sunhome integration isn't installed when you add PowerSync, the setup flow exits cleanly with a direct pointer to HACS. The dependency is soft — PowerSync continues to work normally for all other battery brands whether or not ESY Sunhome is present.

*Update available via HACS*
