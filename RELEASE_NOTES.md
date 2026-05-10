<!-- release: v2.12.358 -->

## What's Changed

**NeoVolt force charge stays active for the requested window**
PowerSync now refreshes NeoVolt force-charge dispatch while a PowerSync force-charge timer is active. This keeps NeoVolt systems from dropping back to Normal early when the upstream NeoVolt bridge arms a shorter inverter-side dispatch timeout than the duration selected in PowerSync.

**Restore state remains correct during NeoVolt refreshes**
The refresh path preserves the original per-inverter restore modes instead of recapturing temporary Force Charge or No Battery Charge states. Multi-stack NeoVolt systems can keep the lower-SOC stack charging while the higher-SOC stack is parked, then restore cleanly when the PowerSync force window ends.

Update available via HACS
