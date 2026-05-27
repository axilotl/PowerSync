<!-- release: v2.12.491 -->

## What's Changed

**SolarEdge dashboard sensors survive Home Assistant entity renames**
The generated PowerSync dashboard now finds HA-composed PowerSync sensor IDs such as `sensor.powersync_amber_battery_level`, not only the older `sensor.power_sync_*` names. This restores SolarEdge battery level and related live-status cards for installs where Home Assistant names entities from the integration or device label.

**SolarEdge command-mode discovery accepts more entity names**
SolarEdge battery dispatch now recognizes additional writable command-mode aliases, including `remote_command_mode`, so installs exposing the storage control bridge under those names can become fully controllable without custom entity renaming.

Update available via HACS
