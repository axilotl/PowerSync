<!-- release: v2.12.476 -->

## What's Changed

**Fix non-Tesla mobile export breakdowns**
PowerSync now splits aggregate grid export between available solar export and battery export before filling the Tesla-style detail fields used by the mobile app. This prevents FoxESS, Flow Power, and other non-Tesla energy-summary systems from showing impossible solar detail values such as "To Grid" being higher than total solar generation.

Update available via HACS
