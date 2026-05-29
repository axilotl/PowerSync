<!-- release: v2.12.497 -->

## What's Changed

**SolarEdge daily import/export totals use the real day baseline**
SolarEdge M1 import/export entities are lifetime counters, so PowerSync now uses Home Assistant recorder history to recover the local-midnight counter value before calculating today's grid import/export. This fixes mid-day startup or restart cases where the dashboard could undercount daily grid import after the baseline was captured too late, and it also corrects already-stored same-day baselines when recorder data has a better midnight value.

**Solar surplus EV charging respects stop-delay hysteresis**
Parallel solar-surplus EV charging now keeps the session active through the configured stop-delay window when reserved surplus temporarily disappears below the battery floor. Short dips no longer cause an immediate pause before the normal low-surplus hysteresis has a chance to absorb the change.

Update available via HACS
