<!-- release: v2.12.316 -->

## What's Changed

**SAJ H2 force charge now uses TOU charge slot 7**
Force charge on SAJ H2 systems now uses the same schedule-driven method as force discharge, but through charge slot 7. PowerSync programs charge slot 7 for the full day at 100%, enables that slot in TOU mode, and temporarily clears conflicting discharge slots so the inverter is driven through the path that reliably starts high-rate charging.

**Restore normal returns SAJ systems to Self-Use**
Restoring normal operation now clears PowerSync's charge and discharge slot-7 bits, restores any cached user slot configuration, turns off leftover passive/manual switches, and finishes by writing AppMode 0 so the inverter returns to Self-Use mode after a force operation.

Update available via HACS
