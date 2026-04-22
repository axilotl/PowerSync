## What's Changed

**Follower PW3 Battery Health — Inferred from Aggregate**
The leader gateway's `DeviceControllerQuery` response returns `None` BMS signal values for follower Powerwall units regardless of whether the query goes through the local gateway or Fleet API relay. The follower's capacity is, however, derivable: `systemStatus.nominalFullPackEnergyWh` (the authoritative site total) minus the sum of all leader pack capacities equals the follower's contribution. The serial number is extracted from `batteryBlocks[].din`. The follower unit now displays its real capacity (~14.4 kWh) and charge level in the battery health screen, with its serial number correctly shown. For systems with multiple follower units the remaining energy is split evenly among them.

Update available via HACS
