<!-- release: v2.12.589 -->

## What's Changed

**Flow Power curtailment uses the actual export tariff**
GoodWe and other inverter curtailment checks now use PowerSync's generated Flow Power tariff schedule before falling back to raw AEMO coordinator prices. This keeps solar curtailment aligned with Flow Power's real export credit, so outside Flow Happy Hour it no longer treats the raw wholesale feed-in value as the amount the user is paid to export.

Update available via HACS
