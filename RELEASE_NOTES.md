<!-- release: v2.12.611 -->

## What's Changed

**GoodWe idle no longer rewrites on-grid DOD**
Smart Optimization idle periods on GoodWe systems now return the inverter to self-consumption without using the GoodWe on-grid DOD setting as a temporary SOC hold. This prevents Flow Power and other optimized schedules from leaving GoodWe DOD at values such as 20% after an idle hold, missed restore, or Home Assistant restart, while preserving explicit force charge, force discharge, and scheduled EV no-discharge behaviour.

Update available via HACS
