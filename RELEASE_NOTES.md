<!-- release: v2.12.527 -->

## What's Changed

**FoxESS optimizer force-charge recovery**
PowerSync now detects when an optimizer-owned FoxESS force-charge window is still planned but the inverter has dropped back to Self Use and is charging well below the requested target. When that stale hardware state is observed, the optimizer immediately reissues the force-charge command instead of only extending its internal timer, so planned grid charging can recover without waiting for manual intervention.

Update available via HACS
