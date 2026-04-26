## What's Changed

**SAJ H2: Fix force_discharge — number writes after switch writes were resetting passive_discharge_control**
Writing any passive number entity (`passive_bat_charge_power_input`, `passive_bat_discharge_power_input`, `passive_charge_enable_input`) appears to reset the passive switch states as a side-effect, not just `passive_enable`. In the previous fix, `force_discharge` still wrote `charge_power=0` **after** turning on `passive_discharge_control`, which clobbered the switch back to OFF and left the battery idle. Fixed across all four mode functions by moving all number writes before any switch writes — the switch turn_on/turn_off is always the final operation, so it cannot be reset by a subsequent number write. This is the same pattern that made `force_charge` work correctly all along.

Update available via HACS
