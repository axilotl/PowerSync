## What's Changed

**Away Mode: Smarter Load Forecasting After Returning Home**
Away Mode now tracks your departure and return times rather than just a simple on/off flag. When you turn it off on return, the optimizer enters a 7-day recovery window where your vacation-period load data is automatically excluded from forecasts — so the LP uses your normal pre-vacation household patterns instead of near-zero vacation consumption. Previously, returning home left the optimizer with distorted history for up to a week. Departure and return timestamps are persisted across HA restarts so the recovery window survives reboots.

**Profit Maximisation Mode**
A new `switch.power_sync_profit_max_mode` entity lets you tell the LP to prioritise export earnings over battery state-of-charge preservation. When enabled, the LP reduces the value it places on storing charge at day's end and extends the confidence decay horizon from 6 to 12 hours — giving more weight to forecasted price spikes further out. This is useful when you know a profitable export window is coming and want the LP to be more aggressive about discharge rather than conservative.

**Force Discharge: Suppressed False Error Warnings**
During an intentional force discharge (triggered by the app, an automation, or a price spike event), the LP continues running in the background to keep the schedule display up to date. If the discharge drives the battery below the configured optimizer reserve, the LP was logging a WARNING each cycle that appeared as a persistent error in the HA log panel. These messages are now downgraded to INFO during active user-triggered force discharges — the reserve floor is an LP planning concept, not a hard limit on manual export.

*Update available via HACS*
