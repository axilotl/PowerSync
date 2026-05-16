<!-- release: v2.12.413 -->

## What's Changed

**Mobile energy summary fallback for non-Tesla systems**
The Home Assistant calendar-history endpoint now fills the current-day energy row from live PowerSync daily energy sensors when recorder statistics or the coordinator accumulator do not yet have usable values. This fixes Flow Power + FoxESS and other non-Tesla setups where the mobile app could show valid costs but `0 Wh` for generation, import, export, and home consumption.

Update available via HACS
