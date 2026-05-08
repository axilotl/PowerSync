<!-- release: v2.12.344 -->

## What's Changed

**Smoother Home Assistant dashboard flows**
The built-in PowerSync energy flow card now batches Home Assistant state updates into animation frames, reducing jitter when sensors update frequently.

**Preserved SVG flow animation state**
Active flow lines now update their source and direction styling without restarting the dash animation on every state refresh, keeping solar, battery, grid, and EV flows visually smooth.

Update available via HACS
