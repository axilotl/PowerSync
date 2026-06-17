<!-- release: v2.12.669 -->

## What's Changed

**Mark stale energy telemetry unavailable**

PowerSync energy sensors now stop reporting old coordinator values once the backing energy feed has gone stale. This prevents dashboards from continuing to show a last-good solar, grid, battery, or load reading for hours after a Sungrow or other energy coordinator stops updating, making offline telemetry visible instead of misleading.

Update available via HACS
