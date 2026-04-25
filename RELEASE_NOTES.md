## What's Changed

**Fix: Powerwall local signaling log spam for PowerSync proxy users**
Users connecting via the PowerSync.cc proxy (psync_ tokens) saw repeated errors every few seconds — "all hermes JWT exchange endpoints failed" and "HermesServer rejected raw token fallback" — looping indefinitely. The signaling WebSocket requires a real Tesla JWT with hermes scope, which psync_ proxy credentials can't provide directly. The client now gives up cleanly after 3 consecutive failures instead of retrying forever. Additionally, if the `tesla_fleet` Home Assistant integration is installed alongside PowerSync, its real Tesla access token will now be used for signaling (which does have the right scopes), making signaling functional for psync_ users who have both integrations.

*Update available via HACS*
