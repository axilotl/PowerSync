<!-- release: v2.12.325 -->

## What's Changed

**Neovolt legacy config expansion**
Existing PowerSync installs that were configured before multi-inverter Neovolt support now automatically use all installed Neovolt inverter entries at runtime. This prevents older single-entry configurations from showing zero battery, load, grid, and solar flow when the originally selected inverter has no live states.

**Neovolt partial-state fallback**
The Neovolt fleet reader now keeps publishing data from available inverters even when another registered inverter entry is temporarily missing live Home Assistant states, so the dashboard does not collapse to an empty/loading flow.

Update available via HACS
