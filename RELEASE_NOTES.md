<!-- release: v2.12.335 -->

## What's Changed

**Fix matched EV name in the Home Assistant dashboard**
The built-in PowerSync energy flow dashboard now uses the backend-matched active EV name from the PowerSync EV sensor instead of guessing from the first Tesla charge-cable entity Home Assistant returns. This keeps multi-Tesla dashboards aligned with the Wall Connector VIN and mobile app, so the charging car is labelled correctly.

**Refresh the dashboard bundle**
The dashboard JavaScript cache version was bumped so Home Assistant requests the updated energy flow strategy after the release is installed.

Update available via HACS
