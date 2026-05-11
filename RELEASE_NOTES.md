<!-- release: v2.12.387 -->

## What's Changed

**Restore the optimiser reserve as a hard discharge floor**
PowerSync now stops forced/max discharge for every battery system when SOC reaches the optimiser reserve and returns the inverter to self-consumption. This restores the intended behaviour for FoxESS and other Modbus systems: the optimiser reserve is the floor for both export and normal optimiser-driven discharge decisions.

Update available via HACS
