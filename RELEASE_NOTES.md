<!-- release: v2.12.666 -->

## What's Changed

**Hold the export floor through projected home-load slots**

Smart Optimization now keeps the active export floor in force when building the displayed schedule after a battery export window. This prevents the plan from showing a sharp projected SOC drop below the export floor immediately after export stops, and uses hold mode once the floor is reached instead of synthesising extra home-load discharge below that floor.

Update available via HACS
