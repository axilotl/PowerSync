## What's Changed

**Follower PW3 Battery Health Data**
In a leader+follower PW3 configuration, the leader's `DeviceControllerQuery` response includes only a placeholder (no signal values) for the follower inverter unit's battery module. PowerSync now sends a second signed query directly to the follower's DIN after the leader query completes. If the site-level RSA key is accepted by the follower unit, its real capacity and charge level will appear in the battery health screen instead of showing 0 kWh. If the follower query fails or times out, the existing behavior is preserved with a warning in the HA log.

Update available via HACS
