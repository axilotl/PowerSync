<!-- release: v2.12.501 -->

## What's Changed

**Show planned battery windows on the optimizer dashboard**

The optimizer dashboard now surfaces upcoming battery charge, discharge, and export windows directly, including timing, duration, SOC range, power, and price context where available. This makes the plan easier to scan without needing to infer important battery actions from the full 24-hour chart.

**Keep monitoring mode from restoring battery control on shutdown**

When Smart Optimization is disabled while monitoring mode is active, PowerSync now stops the executor without forcing the battery back to normal operation. This keeps monitoring-only sessions from unexpectedly changing inverter mode during shutdown or disable flows.

**Avoid interrupting optimizer-owned force modes**

Tariff sync is allowed to continue while the optimizer owns an active force mode, but price-update re-optimization is now skipped during that active optimizer force window. This prevents repeated LP refreshes from fighting the force command while still allowing tariff updates to run.

**Respect the Spread Import setting in free windows**

Free import windows are no longer automatically flattened when Spread Import is off. Users on tariffs such as Globird ZEROHERO can now leave Spread Import disabled and allow PowerSync to request higher-rate charging during the free window instead of silently averaging the charge across the whole period.

Update available via HACS
