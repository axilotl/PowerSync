<!-- release: v2.12.323 -->

## What's Changed

**Neovolt multi-inverter support**
PowerSync now supports selecting and controlling multiple Neovolt/Bytewatt inverter entries from the Neovolt Modbus integration. Force charge, force discharge, restore normal, backup reserve, and idle commands are sent to every selected inverter instead of only the first configured entry.

**Fleet-level battery readings**
Neovolt readings now represent the whole battery fleet: power, grid, load, solar, capacity, and dispatch limits are combined across selected inverters, while SOC and SOH are capacity-weighted so dashboards and optimizer decisions reflect the full system.

Update available via HACS
