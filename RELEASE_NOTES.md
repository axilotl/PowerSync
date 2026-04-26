## What's Changed

**SAJ H2: Fix restore_normal — passive_enable=2 alone is insufficient, switch must also be ON**
Setting `passive_charge_enable_input = 2` (from 2.12.185) brings the battery back into discharge mode but at a reduced rate. Full self-consumption recovery requires both `passive_enable = 2` AND `passive_charge_control` switch ON — the switch only sticks when passive_enable is non-zero, so the order matters. `restore_normal()` now sets `passive_enable = 2` first, then turns on the charge switch.

Update available via HACS
