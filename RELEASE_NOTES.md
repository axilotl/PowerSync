<!-- release: v2.12.347 -->

## What's Changed

**Flow Power TWAP calculation fix**
Flow Power import prices and generated tariff schedules now use the raw rolling wholesale TWAP required by the PEA formula. Portal TWAP remains available as an account metric, but it is no longer substituted into PEA calculations where it could make prices read too low.

**Endeavour Energy N73 tariff support**
PowerSync now requires `aemo-to-tariff` 0.7.15 or newer, which includes upstream Endeavour Energy N73 tariff support. N73 can appear in the Flow Power network tariff selector after Home Assistant installs the updated dependency.

Update available via HACS
