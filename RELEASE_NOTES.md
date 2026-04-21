## What's Changed

**GloBird Setup Failure Fixed (HTTP 403 on Restart)**
GloBird (and other custom-tariff) entries that had a stale Amber API token stored from a previous configuration were crashing on every HA restart with "Failed setup, will retry: Client error 403". The integration was unnecessarily creating an Amber price coordinator for these entries, which hit the Amber API with an expired token and raised `ConfigEntryNotReady`. The Amber coordinator is now only initialised for providers that actually use Amber pricing (Amber, Flow Power).

**Amber Token Rotation Now Reveals Site Picker**
When updating an expired Amber API token via Configure → Pricing → Amber, the new token is now validated immediately on submit. If valid, the form re-renders with the Amber site dropdown populated — so users with an expired token can update it and select their site in a single flow. Previously the form would save and exit without ever showing the site picker if the existing token was invalid.

Update available via HACS
