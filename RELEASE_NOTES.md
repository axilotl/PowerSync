## What's Changed

**SAJ H2: Fix restore_normal — passive_enable=2 was resetting the discharge switch**
The stanus74 integration resets both `passive_charge_control` and `passive_discharge_control` switches to OFF whenever `passive_charge_enable` is written. `restore_normal` was writing `passive_enable=2` as the last step, which silently clobbered the `passive_discharge_control=ON` set in the previous step — leaving the battery in exactly the same blocked state as force_charge. Fixed by writing `passive_enable=2` first in all four mode functions (force_charge, force_discharge, set_idle, restore_normal), so subsequent switch writes are not reset. All modes now work correctly.

Update available via HACS
