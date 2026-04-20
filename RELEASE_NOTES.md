## What's Changed

**Force Discharge Duration Now Respected from All Sources**
Automations created via the web app stored the duration as `minutes`, while the HA automation executor only read `duration` and `duration_minutes`. This caused force discharge automations configured for 60 minutes to terminate at 30 minutes (the hardcoded default). The executor now reads all three field names so automations from the web app, mobile app, and direct HA service calls all honour the configured duration.

**Force Charge Duration Consistency**
The same field-name gap affected force charge automations. The fix applies to both action types, ensuring the configured duration is respected regardless of which client created the automation.

Update available via HACS
