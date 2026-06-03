<!-- release: v2.12.562 -->

## What's Changed

**Fix: dashboard refreshing every ~5 minutes**
With Auto-Apply Optimizer Reserve enabled, the optimiser recalculated a forecast reserve floor each cycle and saved it to its configuration whenever it changed — roughly every 5 minutes. That wasn't a full integration reload (it never restarted everything), but writing the configuration that often made Home Assistant refresh the dashboard on a 5-minute loop. The forecast reserve is now applied to the running optimiser directly without rewriting the saved configuration, so the dashboard stays put. Your live reserve still shows correctly in sensors and the mobile app, and it's recalculated within one cycle after any restart.

Update available via HACS
