<!-- release: v2.12.432 -->

## What's Changed

**Auto-detect GoodWe EMS entity prefixes**
PowerSync now scans Home Assistant for a matching GoodWe EMS mode and EMS power-limit entity pair when Home Assistant entity control is selected. If a stale prefix such as `goodwe_esa` is entered but Home Assistant now exposes `select.goodwe_ems_mode` and `number.goodwe_ems_power_limit`, PowerSync resolves and saves the working `goodwe` prefix instead of falling back with `goodwe_ems_entities_missing`.

**Reduce setup friction for GoodWe LAN / Kit-20 users**
The GoodWe setup and options flows now use the detected EMS prefix consistently across initial setup, connection settings, and GoodWe settings, with updated help text explaining that PowerSync can auto-detect the required entity pair.

Update available via HACS
