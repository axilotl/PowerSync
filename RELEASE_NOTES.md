<!-- release: v2.12.352 -->

## What's Changed

**Safari energy-flow flicker reduced**
The built-in PowerSync energy-flow card now uses WebKit-safe SVG image handling and avoids SVG repaint hotspots that could make the animated house scene flicker constantly in Safari on macOS. The card keeps the same layout while reducing expensive background repaints during live Home Assistant state updates.

**48-hour load forecast tails restored**
PowerSync no longer treats a short HAFO load forecast as a complete 48-hour forecast by flat-padding the missing tail. When HAFO only covers part of the window, PowerSync now uses HAFO for the real coverage and fills the uncovered tail from historical load patterns so the LP Forecast chart keeps realistic load values across the full window.

Update available via HACS
