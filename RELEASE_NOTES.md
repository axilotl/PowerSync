<!-- release: v2.12.281 -->

## What's Changed

**Fix Tesla BLE plug detection**
PowerSync no longer treats an existing Tesla BLE charger switch as proof that a vehicle is home or plugged in. BLE vehicles now use current charge-flap, charging-state, measured charge-power, charger-on, or recent plug-cache evidence, preventing away or unplugged cars from being scheduled as if they were connected.

**Stop phantom EV charging in the app**
Stale BLE charging sessions are now released when the vehicle is definitively unplugged, and loadpoint status uses measured BLE vehicle power instead of commanded amps. The dashboard and EV loadpoint views should no longer show cars drawing phantom kW when Home Assistant reports the BLE charger switch as off.

Update available via HACS
