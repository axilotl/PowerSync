<!-- release: v2.12.590 -->

## What's Changed

**Tesla TOU mode changes are now verified**
PowerSync now reads back Tesla operation mode changes after both paired local Powerwall writes and cloud Tesla writes. If Tesla accepts a request but does not actually report the expected mode, PowerSync fails the service call so automations can retry instead of silently treating the mode change as complete. For TOU/autonomous mode it also attempts the same self-consumption to autonomous recovery bounce used by other Tesla control paths.

**Generic charger entities can be cleared**
EV charging settings now persist blank generic charger entity fields when a user clears them. This prevents stale switch, amps, status, or SOC entities from staying in the saved configuration after they have been removed from the options flow.

Update available via HACS
