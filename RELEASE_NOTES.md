## What's Changed

**Sensors now grouped into logical sub-devices in Home Assistant**
All PowerSync entities are now organised into named sub-devices under the main PowerSync hub: Battery, Solar & Inverter, LP Optimizer, Grid & Home, Pricing & Cost, EV Charging, Flow Power, AEMO, and more. Previously everything appeared as one flat list of 50+ entities. Sub-devices appear in the Home Assistant device registry and make it much easier to navigate to the sensors you care about.

**Corrected Sigenergy Modbus register addresses for rated charge/discharge power**
The ESS rated charging power (30068) and rated discharging power (30070) addresses have been corrected against the official Sigenergy Modbus Protocol v2.7. The previous attempt used addresses from an unofficial source that placed them in the Reserved block (30073–30082), causing persistent ILLEGAL_DATA_ADDRESS Modbus errors. Rated energy capacity (30083) and SOH (30087) were already correct and are unchanged.

**Fixed redundant Sigenergy TOU re-sync on every price interval**
The Stage 4 (60-second) price check was always triggering a full Sigenergy Cloud API tariff sync, even when Stage 3 (35-second) had already completed it moments earlier. The price-change tracking wasn't being recorded after Sigenergy syncs, so Stage 4 always saw "no previous price" and re-synced unnecessarily. This wasted API calls and caused duplicate LP optimizer runs each interval.

*Update available via HACS*
