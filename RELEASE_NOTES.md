<!-- release: v2.12.459 -->

## What's Changed

**FoxESS entity bridge for foxess_modbus**
PowerSync can now connect to FoxESS systems through Nathan Marlor's existing `foxess_modbus` Home Assistant integration. This avoids opening a second direct Modbus session to the inverter while still reading solar, grid, battery, load, SOC, SOH, PV string, reserve, temperature, and daily energy data.

**FoxESS controls through Home Assistant entities**
The new bridge sends supported FoxESS commands through existing Home Assistant entities, including force charge, force discharge, restore to self-use, backup reserve, work mode, charge/discharge current limits, and export-limit curtailment when that entity is available. Setup validation now reports missing required bridge entities clearly.

Update available via HACS
