<!-- release: v2.12.418 -->

## What's Changed

**Fix stale Tesla reserve self-heal source**
PowerSync now reads the live Tesla site_info backup reserve before the Home Assistant backup-reserve number entity when the optimizer starts. This prevents a stale stored `_user_backup_reserve` value from being compared against itself, so the v2.12.417 startup cleanup can correctly replace old IDLE-derived reserve values with the real Powerwall reserve.

Update available via HACS
