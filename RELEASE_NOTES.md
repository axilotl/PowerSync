## What's Changed

**SAJ H2: Fix force_charge — charge register is percentage-based (0–1100), not watts**
Both `passive_battery_charge_power_input` and `passive_battery_discharge_power_input` use the same 0–1100 scale (percent of rated power × 10, not watts). `force_charge()` was calling `number.set_value` with a watt value (e.g. 3000W), which exceeded the entity's max of 1100 and failed HA validation — leaving the inverter in self-consumption while PowerSync's mode tracker showed `force_charge`. Fixed: `force_charge()` now sets the register to 1100 (full rate), matching how `force_discharge()` works.

Update available via HACS
