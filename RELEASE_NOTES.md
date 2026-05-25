<!-- release: v2.12.472 -->

## What's Changed

**Fix FoxESS mobile energy summaries returning empty rows**
The Home Assistant calendar-history endpoint now correctly treats the current day as included when the request ends at the current time. This fixes FoxESS and other non-Tesla setups where the mobile app could call the right endpoint but receive `rows=0`, leaving the day energy detail screens at 0 Wh even though live inverter totals were available.

**Respect target-export power caps without under-counting discharge capacity**
Smart Optimization now separates the user export-command cap from the battery's physical discharge capability for target-export systems including GoodWe, Sigenergy, Sungrow, FoxESS, AlphaESS, Solax, SAJ H2, Fronius Reserva, and NeoVolt. Export plans can still cover home load while limiting commanded grid export to the configured cap, and spread-export calculations now use the actual export command power.

Update available via HACS
