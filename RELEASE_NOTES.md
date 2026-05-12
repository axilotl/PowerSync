<!-- release: v2.12.391 -->

## What's Changed

**Stop OCPP EV charge sessions being over-counted**
PowerSync now leaves OCPP charge-session energy and cost tracking to the OCPP session poll, instead of also adding estimated dynamic-control readings from the requested amp limit. This fixes inflated EV charging totals when PowerSync is controlling an OCPP charger and the charger is already reporting metered session power.

Update available via HACS
