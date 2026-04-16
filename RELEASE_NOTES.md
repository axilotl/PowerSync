## What's Changed

**Fix: curtailment error "name 'entry_data' is not defined"**
Resolves a `NameError` that appeared in the Home Assistant log as `Error applying curtailment: name 'entry_data' is not defined` whenever solar curtailment triggered on a system without AC-coupled inverter curtailment configured (common for Tesla-only, DC-coupled, or unsupported-brand installs). The off-grid fallback branch referenced a variable that was never bound in its scope, causing the curtailment apply to abort before the Powerwall off-grid fallback or export-rule change could run. Curtailment now completes cleanly on these setups.

Update available via HACS
