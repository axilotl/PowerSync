## What's Changed

**Tesla Powerwall — New Backup-Only Operation Mode**
The Operation Mode picker now offers a third option: Backup-Only. This mode keeps the Powerwall reserved for outage protection and stops it from following Time-of-Use or self-consumption logic. Useful for sites that want the battery purely as a UPS without participating in arbitrage. Available via the Operation Mode select entity, the `set_operation_mode` service, and the mobile app.

**Tesla Powerwall — Live Telemetry Sensors**
Six new sensors expose detail that previously lived only in Tesla's API: Battery Pack Capacity (nameplate kWh), Battery Energy Left (kWh derived from SOC × capacity), Backup Time Remaining (estimated hours at the current home load), Grid Services Power (kW being dispatched for VPP), and three diagnostic flags — Grid Services Active, Calibration Active, and Permission to Operate. Backup Time Remaining is the headline addition: it answers "how long can my house run on the battery right now?" without manual math.

**Tesla Powerwall — Lifetime Energy Totals**
Six new total-increasing sensors track lifetime Solar Generated, Grid Imported, Grid Exported, Battery Charged, Battery Discharged, and Home Consumption, summed from Tesla's calendar history endpoint and refreshed hourly. Compatible with the HA Energy dashboard for long-term usage analysis. Values populate on first successful fetch — expect the first hour after restart to show "unknown".

**Local TEDAPI — Per-Powerwall Sensors (PW2 firmware)**
Sites with the local Powerwall gateway paired now get richer telemetry from the gateway directly. New system-level sensors: System Island State (richer than the simple grid_status), Powerwall Count, Active Alerts (with alert names exposed as attributes), and Powerwall Alert Active (binary problem indicator). Per-Powerwall sensors discovered automatically: SOC, Capacity, Voltage, Temperature, and State of Health for each in-service unit. PW3 firmware does not expose the legacy endpoint these read from — sites on PW3 will silently skip these sensors without errors.

**New Service: Schedule Max Backup**
A new `power_sync.schedule_max_backup` service charges the Powerwall to 100% for a fixed window (1–1440 minutes), then automatically restores the previous backup reserve when the window ends. Use ahead of forecast outages or storms. The schedule survives Home Assistant restarts — if HA reboots mid-window, the schedule resumes for the remaining time, or restores immediately if the window expired during downtime. Calling the service while another window is active replaces the schedule and preserves the original baseline reserve so back-to-back calls don't lose your normal setting.

**New Service: Refresh Calibration**
The new `power_sync.refresh_calibration` service clears the integration's calibration_suspected flag. Useful after a Powerwall calibration cycle completes if the optimiser hasn't auto-cleared the flag, or to force-retry mode toggles immediately. Doesn't touch the Powerwall — purely resets PowerSync's local guard.

**Device Tree Reorganisation**
Powerwall-specific sensors now live on dedicated Home Assistant devices instead of the main PowerSync entry: a "Tesla Powerwall" device for site-level telemetry, with sub-devices ("Powerwall 1", "Powerwall 2", …) for each in-service unit. Controls (backup reserve, operation mode, grid export, force charge/discharge) and primary energy sensors stay on the main PowerSync device. Existing entities remain on their current device — only the new sensors introduced in this release populate the new hierarchy.

**Dynamic Dashboard Updates**
The auto-generated dashboard surfaces all of the above where it makes sense: new status badges (Grid Services Active, Calibration Active, Permission to Operate) join the existing Tesla controls section, a Powerwall Status card shows backup runtime and capacity, a Lifetime Energy card displays the new totals, and a Powerwall Health section auto-builds per-PW cards when local pairing reports multiple units. Every section is gated on entity existence so single-Powerwall and PW3 sites only see relevant cards.

Update available via HACS
