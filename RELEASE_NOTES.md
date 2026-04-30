## What's Changed

**EV charging now stops even when PowerSync didn't start it**
Fixed a bug where Teslas that auto-started charging on plug-in (the default Tesla firmware behaviour) would keep drawing power indefinitely. PowerSync only tracked stop logic against its own internal "did I start this?" flag — so when conditions said charging should stop (price, SoC, schedule), nothing happened. Now the planner probes the vehicle's actual charging state via Teslemetry BT, Tesla Fleet, or BLE entities and sends the stop command whenever the car is drawing power, regardless of who initiated it. This also fixes the reload scenario where the in-memory "is charging" flag was wiped while the car kept charging.

**Better diagnostics when hermes signaling auth fails**
When the local Powerwall signaling channel can't get a hermes JWT, the warning log now includes the parsed error code, the access token's actual scopes, and up to 400 characters of Tesla's response detail (previously truncated at 200, hiding the most useful diagnostic — `token_scopes`). Makes it possible to tell at a glance whether a 412 from Tesla is a missing-scope issue on your token or a Tesla-side change.

Update available via HACS
