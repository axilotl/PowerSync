## What's Changed

**OCPP Charger Detection Compatibility Fix**
Resolved a crash affecting users with OCPP EV chargers on recent Home Assistant versions. The integration was using a deprecated `hass.helpers.entity_registry` API that was removed from modern HA, causing an `AttributeError` during OCPP charger detection at startup. Updated to use the current `homeassistant.helpers.entity_registry` import style — no change in behaviour, just restored compatibility.

Update available via HACS
