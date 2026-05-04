<!-- release: v2.12.279 -->

## What's Changed

**Powerwall pack sensors now use the BMS health scan**
Individual Powerwall pack entities now read from the same BMS health scan used by Battery Health, so SOC, capacity, and state of health populate from real leader, follower, and expansion-pack data instead of the shallow battery block count that produced unknown values.

**Expansion packs stay under Tesla Powerwall**
Expansion modules are now surfaced as pack-level sensors under the aggregate Tesla Powerwall device, keeping the Home Assistant device page tidy while still showing each pack. PowerSync also skips voltage and temperature pack sensors unless the BMS scan includes those metrics, avoiding empty entities.

Update available via HACS
