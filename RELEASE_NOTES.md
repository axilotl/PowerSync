<!-- release: v2.12.367 -->

## What's Changed

**Dual Sungrow force discharge limits**
Dual Sungrow setups now publish combined charge and discharge limits from both inverters and use each inverter's own maximum discharge limit when a force discharge request is at the combined maximum. This avoids under-driving one side of a paired Sungrow system when users request full discharge output.

**Neovolt restore-mode preservation**
Neovolt force discharge calls now pass the restore-mode preservation flag through the energy coordinator, so hardware extension flows can keep the intended restore behavior instead of dropping that option at the coordinator boundary.

Update available via HACS
