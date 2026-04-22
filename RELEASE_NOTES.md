## What's Changed

- Solax battery setup now selects a specific `solax_modbus` integration entry instead of relying on a free-text entity prefix.
- PowerSync now discovers Solax entities from the selected integration entry and handles known mode-select naming variants more robustly.
- Existing legacy prefix-based Solax entries continue to load, while new setups and options use the safer config-entry bridge path.

Update available via HACS
