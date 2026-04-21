## What's Changed

**Dashboard Strategy Timeout Fix**
Bumps the frontend JS cache key to force browsers to load the latest strategy file. If you saw "Timeout waiting for strategy element" after updating to v2.12.102 or v2.12.103, this resolves it — the old cached JS was being served instead of the updated file. Restart HA after updating, then do a hard browser refresh (Cmd/Ctrl+Shift+R).

Update available via HACS
