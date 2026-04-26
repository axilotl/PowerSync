## What's Changed

**SAJ H2: Fix sensors permanently stuck at 0.0 — entity discovery was never being called**
`SajH2EnergyCoordinator._async_update_data()` was calling `get_status()` directly without ever calling `connect()`, which is the method responsible for running entity discovery. As a result, `_entity_map` was always empty, every `_read_float()` returned None, and all PowerSync sensors (battery level, battery power, grid power, solar power, home load) reported 0.0 permanently — even after the correct key mappings were applied in 2.12.183. Entity discovery now runs lazily on the first coordinator update if the map is empty.

Update available via HACS
