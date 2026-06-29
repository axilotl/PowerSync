<!-- release: v2.12.735 -->

## What's Changed

**No-idle mode now applies to monitoring-mode dry runs**
PowerSync now applies the no-idle override before the monitoring-mode execution guard. This keeps the optimizer's dry-run status aligned with live execution, so Flow Power and other supported TOU plans report `self_consumption` instead of `idle` when "Disable idle mode" is enabled.

**Tesla force-discharge refresh no longer drops saved state**
Tesla optimizer-owned force-discharge refreshes now reuse the saved per-site restore state from the active force session. This prevents repeated force-discharge tariff refreshes from failing with a `saved_states` local-variable error while the optimizer rolls a Tesla export window forward.

Update available via HACS
