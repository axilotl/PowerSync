<!-- release: v2.12.286 -->

## What's Changed

**Stop Octopus Saving Sessions GraphQL errors**
PowerSync no longer polls the removed Kraken `savingSessions` query or the removed direct join mutation. This fixes the repeated Home Assistant 400 errors seen after Octopus retired those Saving Sessions fields from their GraphQL API.

**Keep Free Electricity events working in direct mode**
Direct Octopus mode now resolves the account's electricity supply point and passes the required identifier when fetching Free Electricity campaign events. Free Electricity sessions can still be detected, while direct Saving Sessions auto-join now clearly points users to the octopus_energy/Bottlecap Dave source that still exposes those events.

Update available via HACS
