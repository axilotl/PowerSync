<!-- release: v2.12.506 -->

## What's Changed

**Fix local Powerwall home load while EV charging**
PowerSync now subtracts observed EV charging power from the paired local Powerwall home-load reading. This keeps the Home Load sensor and dashboard aligned with the Tesla app when a Wall Connector or vehicle charge session is active, instead of showing the EV charging load twice as both EV Power and Home Load.

Update available via HACS
