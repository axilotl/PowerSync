<!-- release: v2.12.630 -->

## What's Changed

**Fix scheduled charging stops for second Tesla vehicles**
PowerSync now identifies which Tesla is physically charging before stopping an external scheduled-charging session outside the allowed window. In multi-Tesla setups, the stop command is routed to the active vehicle instead of falling back to the first configured Tesla.

Update available via HACS
