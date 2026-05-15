<!-- release: v2.12.408 -->

## What's Changed

**Sigenergy EVAC app visibility**
Configured Sigenergy EVAC and EVDC chargers now appear in the PowerSync app vehicle list, EV dashboard widget, and normalized loadpoint status. Previously the charger settings could be saved and used for control actions, but the app/dashboard had no observation path for Sigenergy chargers, so users saw no visible change after reload or restart.

**Offline charger state**
If PowerSync cannot read the configured Sigenergy charger over Modbus, the app now shows the charger as unavailable instead of hiding it entirely. This makes bad IP, port, or slave-ID configuration visible during setup.

Update available via HACS
