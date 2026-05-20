<!-- release: v2.12.441 -->

## What's Changed

**EV charging no longer reserves the full home-battery charge rate by default**
Price-level opportunity charging and Smart Schedule grid charging now start EV sessions with a zero home-battery charge target unless a mode explicitly asks to preserve battery charging. PowerSync still passes through the inverter and battery charge-rate capabilities for limit calculations, but EV charging no longer silently holds back the optimizer's full battery charge rate.

**Solar surplus below the battery floor is strict surplus only**
Solar surplus EV charging may now run below the configured home-battery floor only while the battery is still charging and surplus remains after the battery reserve. If the battery starts discharging into the car, or EV charging causes grid import beyond tolerance, PowerSync immediately backs the EV down to zero amps and logs the strict-surplus pause reason.

**Smart Schedule uses Sigenergy EVAC and EVDC as first-class chargers**
Smart Schedule now resolves Sigenergy charger host, port, slave ID, and charger type through the same configured charger path used by price-level charging. Sigenergy EVAC and EVDC starts route through the Sigenergy Modbus charger backend instead of falling back to Tesla vehicle discovery.

Update available via HACS
