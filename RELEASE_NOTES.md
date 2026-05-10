<!-- release: v2.12.373 -->

## What's Changed

**GoodWe hardware reserve saves now survive restart cleanly**
PowerSync now keeps the saved hardware reserve in sync across both Home Assistant config stores when it is changed through the app or API. This fixes GoodWe systems where the user could set a 20% reserve and 80% on-grid DOD, but after restarting Home Assistant PowerSync would display the old 45% reserve and write GoodWe back to 55% DOD.

Update available via HACS
