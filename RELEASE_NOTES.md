<!-- release: v2.12.396 -->

## What's Changed

**Fix Home Assistant energy-flow flicker on short paths**
The built-in PowerSync energy-flow card now adapts each animated SVG flow line to the actual path length. This prevents short battery, grid, and home flow segments from blinking fully off as the dash animation moves, while keeping the existing animation style on longer paths.

**Refresh dashboard frontend assets**
The dashboard JavaScript cache version was bumped so Home Assistant reloads the updated energy-flow card after the HACS update instead of continuing to serve a stale frontend bundle.

Update available via HACS
