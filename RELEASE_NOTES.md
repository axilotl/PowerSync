<!-- release: v2.12.481 -->

## What's Changed

**Expose per-battery Powerwall current energy**
PowerSync now creates a dedicated `Current Energy` sensor for each BMS-discovered Powerwall pack, using the same per-pack remaining-energy data shown in the Tesla app. This makes the value available as normal Home Assistant entities instead of only as hidden pack attributes or aggregate site energy.

**Fix SolarEdge runtime startup**
SolarEdge battery-system setups now bypass Tesla credential initialization during startup, so active-power curtailment sites can initialize without requiring Tesla API details.

**Restore GloBird ZeroHero settings persistence**
The provider config API now returns and saves the GloBird ZeroHero plan fields used by setup and options flows, and the UI copy now describes the 0.09 kWh evening import allowance more accurately.

Update available via HACS
