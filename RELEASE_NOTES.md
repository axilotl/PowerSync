## What's Changed

**Enphase DPEL: read-modify-write to satisfy all required fields**
2.12.38 added `installed_capacity` to the DPEL payload, which fixed the original silent failure but uncovered a second required field (`relay_config`). Rather than playing whack-a-mole with whatever extra fields each firmware version demands, PowerSync now reads the gateway's existing DPEL settings, modifies just the values it needs to change, and posts the full merged payload back. Whatever fields your gateway returned in the GET will be echoed in the POST, so future firmware additions won't break curtailment.

**Disable-DPEL fallback no longer claims false success**
The historic fallback "if DPEL POST is rejected, disable DPEL entirely" only works on installs whose base grid profile is already zero-export. On most Australian installs, the base profile allows full export — so disabling DPEL was actually turning curtailment off and logging "Successfully curtailed (disabled, using profile)". This fallback now only runs for explicit zero-export mode and is skipped for load-following, which falls through to the DER / AGF profile-switching methods instead.

Update available via HACS
