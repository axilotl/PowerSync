## What's Changed

### Powerwall 2: Off-grid support
PW2 users can now pair and use off-grid / reconnect commands. Previously, pairing always ran the PW3 RSA key registration flow which 404'd on the Tesla Fleet API for PW2 sites. PW2 pairing now validates local gateway connectivity directly — no physical DC isolator toggle needed, no Fleet API key registration. Enter your gateway IP and password, and off-grid is unlocked immediately.

Update available via HACS
