## What's Changed

**Battery Health: Follower PW3 Now Included in Pack Count**
On systems with a PW3 leader + follower, the follower's base module was being excluded from the individual battery pack list because it reports a `None` BMS energy value rather than a real measurement. The pack detection logic now identifies battery modules by the presence of BMS signal keys (regardless of whether the value is populated), so all 4 modules are correctly counted — giving accurate rated capacity and health percentage.

**Solax: Support for `inverter_charger_use_mode` Firmware Variant**
Some Solax wills106 firmware versions use `inverter_charger_use_mode` instead of `charger_use_mode` for the mode select entity. PowerSync now auto-detects which variant is present during setup and uses the correct entity for all charge, discharge, and restore commands. Prefix discovery and the setup error messages have been updated to mention both entity names so the correct prefix is easier to find.

Update available via HACS
