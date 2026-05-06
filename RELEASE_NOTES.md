<!-- release: v2.12.309 -->

## What's Changed

**Sigenergy Amber tariff upload fix**
Sigenergy tariff sync now builds the cloud upload from the same normalized tariff schedule used by the working PowerSync tariff path, then mirrors the final import schedule into Sigenergy's sell-price payload so the Sig app does not display Amber feed-in rates as a second, much smaller tariff. The upload remains enabled for app visibility while PowerSync Smart Optimization continues to control dispatch locally through Remote EMS/Modbus.

**Sigenergy demand settings crash fix**
Fixed a startup/runtime error in the Sigenergy tariff sync helper where demand-charge settings were read from the wrong scope. Sigenergy users should no longer see `cannot access free variable 'demand_charge_rate'` when the tariff sync runs.

Update available via HACS
