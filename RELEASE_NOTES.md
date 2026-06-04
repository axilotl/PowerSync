<!-- release: v2.12.586 -->

## What's Changed

**Generic charger price-level charging now uses the configured charger backend**
Price-level charging now ignores stale Tesla vehicle backend settings when the active loadpoint is the configured generic charger. This prevents generic EV setups from falling into the Tesla Fleet API start path and logging `Could not find Tesla charge switch entity (switch.*_charge)` even though generic charging is enabled.

**Regression coverage for stale charger configs**
Added focused coverage for generic price-level start and stop commands when older saved vehicle charging configs still contain `charger_type: tesla`, so future changes keep routing through the configured switch-based charger.

Update available via HACS
