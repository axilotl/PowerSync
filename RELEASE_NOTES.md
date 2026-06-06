<!-- release: v2.12.602 -->

## What's Changed

**Settings changes reoptimize in the background**
PowerSync now schedules optimizer refreshes after settings updates return instead of running the optimizer inside the settings API response. This keeps dashboard, mobile, and Home Assistant settings changes responsive while still recalculating the plan after changes such as Profit Max, grid charging, optimizer mode, target SOC, target time, and auto reserve tracking.

**Auto reserve toggles avoid duplicate optimizer runs**
Changing forecast-driven reserve tracking now reports whether the reserve state actually changed and shares the same deferred reoptimization path. This prevents redundant immediate optimizer work while still restoring the manual reserve and refreshing the plan when the toggle changes.

Update available via HACS
