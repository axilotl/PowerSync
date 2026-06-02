<!-- release: v2.12.539 -->

## What's Changed

**Auto reserve no longer holds full SOC when there is nothing to protect**
PowerSync now only raises the auto-applied optimizer reserve when the forecast shows a meaningful battery discharge before the next charging opportunity. If the battery is already full and solar surplus is immediate, the optimizer reserve can now return to the saved manual baseline instead of staying pinned near 100%.

Update available via HACS
