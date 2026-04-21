## What's Changed

**Remove Orphaned Sub-Device Groups**
Previous versions (v2.12.97–v2.12.100) introduced device family grouping that split entities into separate sub-devices (PowerSync Battery, PowerSync LP Optimizer, PowerSync Flow Power, etc.). This was reverted in v2.12.101, but the empty sub-devices remained in the HA device registry — appearing on the integration page and in Areas. v2.12.102 adds a one-time cleanup that removes these orphaned devices on integration load.

Update available via HACS
