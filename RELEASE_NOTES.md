## What's Changed

**Sigenergy force discharge now respects the configured DNSP export limit**
The force-discharge path was writing the full battery rated discharge power (e.g. 14.4 kW) directly to the grid export limit register, ignoring the user-configured Sigenergy export limit. During AEMO price spikes and LP-driven exports, this wrote an export ceiling well above the user's DNSP allowance — for households with hardware-enforced 5 kW limits it caused mismatch between the integration's intent and the inverter's enforcement, and for households without hardware enforcement it could have driven over-export. The bypass that was previously needed to avoid a circular dependency with the dynamic safety cap is preserved, but the user-configured DNSP limit is now applied as a hard ceiling on force-discharge writes.

Update available via HACS
