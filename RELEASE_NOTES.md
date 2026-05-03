## What's Changed

**Fix solar curtailment crash on missing Powerwall constant**
The solar curtailment check was raising `NameError: name 'CONF_POWERWALL_OFFGRID_AS_CURTAILMENT' is not defined` on every run because the constant was referenced at runtime but never imported at module load. This produced repeated `ERROR Unexpected error in solar curtailment check` log spam and meant the off-grid-as-curtailment option couldn't actually take effect even when enabled. The missing import has been added — curtailment evaluates cleanly now and the option works as documented.

Update available via HACS
