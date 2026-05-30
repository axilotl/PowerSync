<!-- release: v2.12.507 -->

## What's Changed

**Smarter EV throttling while charging the home battery**
Battery-target EV charging now accounts for solar production, non-EV home load, the configured grid import limit, and the requested Powerwall charge rate together. During free or cheap import windows this helps the EV reduce to the available headroom instead of holding a higher charge rate that prevents the home battery from reaching its target charge power.

**Correct mobile app load readings during EV charging**
The local Powerwall status API now subtracts observed EV charging power from the home-load value it sends to the mobile app, matching the Home Assistant dashboard behavior and avoiding double-counted EV load.

**Merge Tesla Wall Connector and vehicle rows**
Live loadpoints now merge Wall Connector telemetry into the active Tesla vehicle when there is a single safe match. The app should show one EV row with the Wall Connector's current power reading instead of separate Tesla and Wall Connector rows with stale duplicate load.

Update available via HACS
