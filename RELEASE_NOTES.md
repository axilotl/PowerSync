<!-- release: v2.12.519 -->

## What's Changed

**Curtailment now works with custom and static tariffs**
PowerSync can now use the configured tariff schedule as the curtailment price source when no live provider feed-in price is available. This lets FoxESS, Sigenergy, Sungrow, AlphaESS, SolarEdge, GoodWe, Tesla, and AC-coupled inverter curtailment react when export earnings drop below 1c/kWh, even on custom tariffs or non-Amber providers.

**Custom export rates can be negative**
Custom tariff setup now accepts negative export earnings for the default FiT and individual time periods. Use a negative export value when your plan charges you to export, so PowerSync can model those windows correctly and trigger curtailment.

**Curtailment options are battery-system aware**
The options flow no longer shows the Tesla-only Powerwall off-grid fallback for FoxESS and other non-Tesla systems. AC-coupled inverter shutdown remains available for systems that use a separate solar inverter path.

Update available via HACS
