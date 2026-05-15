<!-- release: v2.12.410 -->

## What's Changed

**Fix Solar Surplus EV power accounting**
Solar Surplus now includes measured EV charger power when calculating available surplus, even when PowerSync did not originate the current charging amps. This prevents active Tesla or Wall Connector charging from being ignored as `0.0 kW`, so surplus decisions correctly account for the car before deciding whether to continue, reduce, or stop charging.

**Add EV charger power entity support**
Vehicle charging configuration now carries an optional `charger_power_entity` through scheduling and dynamic control. PowerSync will use that explicit sensor when configured, and for single active Tesla sessions it can fall back to detected Tesla charging power or Wall Connector power sensors.

Update available via HACS
