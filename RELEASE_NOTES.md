## What's Changed

**Away Mode: Smarter Load Forecasting After Returning Home**
Away Mode now tracks your departure and return timestamps instead of a simple on/off flag. When you turn it off on return, the optimizer enters a 7-day recovery window where vacation-period load history is automatically excluded from forecasts — so the LP uses your normal pre-vacation household patterns rather than the near-zero consumption from while you were away. Departure and return times are persisted across HA restarts, so the recovery window survives reboots.

**Profit Maximisation Mode**
A new `switch.power_sync_profit_max_mode` entity lets you tell the LP to prioritise export earnings over battery state-of-charge preservation. When enabled, the LP reduces the value it places on storing charge at day's end and extends the confidence decay horizon from 6 to 12 hours — giving more weight to forecasted price spikes further out. Useful when you want the LP to discharge more aggressively rather than hold charge in reserve.

**Force Discharge: Suppressed False Error Warnings**
During an intentional force discharge, the LP continues running in the background to keep the schedule display up to date. If the discharge drives the battery below the configured optimizer reserve, the LP was logging a WARNING each cycle that appeared as a persistent error in the HA log panel. These messages are now downgraded to INFO during active user-triggered force discharges — the reserve floor is an LP planning concept, not a hard limit on manual export.

**Sungrow SH: Fix Battery Power Sign on Affected Firmware**
On some SH-series firmware versions, register 13022 reports an unsigned battery power value, making charge and discharge indistinguishable. The coordinator's `get_battery_data` path now applies the same fix already in place for the main polling path: it reads the authoritative S32 signed register at 5214–5215 instead, correcting `sensor.power_sync_battery_power` on affected units.

*Update available via HACS*
