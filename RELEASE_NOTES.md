<!-- release: v2.12.495 -->

## What's Changed

**SolarEdge daily grid totals from M1 lifetime counters**
PowerSync now treats SolarEdge `m1_imported_kwh` and `m1_exported_kwh` as lifetime import/export counters instead of direct daily values. The integration stores a daily baseline, restores it after restarts, and reports the current-day delta so dashboards and energy summaries do not show lifetime totals as today-only usage.

Update available via HACS
