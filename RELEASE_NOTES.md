<!-- release: v2.12.488 -->

## What's Changed

**Powerwall spread options hidden**
Powerwall users no longer see the Smart Optimization spread import/export toggles in setup or options, because Tesla Powerwall cannot target a lower output power to the grid for these spread modes. Existing Powerwall configurations are forced back to disabled for both spread settings when the optimization form is saved.

**Supported batteries keep spread controls**
Non-Tesla battery systems still get the spread import/export controls, so target-power systems can continue smoothing planned export and grid-charging windows where the hardware can actually honour those commands.

Update available via HACS
