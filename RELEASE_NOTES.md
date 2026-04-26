## What's Changed

**SAJ H2: House scene and live power sensors now working**
The SAJ H2 battery system was missing from the energy coordinator selection in the sensor platform setup. This meant `sensor.power_sync_solar_power`, `sensor.power_sync_battery_level`, `sensor.power_sync_grid_power`, and related sensors were never registered in Home Assistant — so the app's house scene had no entities to read and showed `--` for all values. SAJ H2 is now correctly wired to its coordinator and all live power sensors are created on startup.

Update available via HACS
