<!-- release: v2.12.664 -->

## What's Changed

**Dashboard tooltip transparency**
The SOC/power and electricity price chart tooltips now use a much lighter explicit alpha surface and no longer apply the heavy blur filter that made the graph behind the tooltip look like a dark solid panel. This keeps the tooltip readable while making the underlying chart lines visibly pass through the tooltip area.

**Dashboard cache refresh**
The dashboard strategy JavaScript cache key has been bumped again so Home Assistant fetches the updated tooltip styling after the HACS update and restart.

Update available via HACS
