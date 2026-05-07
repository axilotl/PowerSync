<!-- release: v2.12.319 -->

## What's Changed

**Smart Optimizer force-command timing**
Smart Optimization now clips optimizer-issued charge and export commands to the current LP action block instead of letting the previous command buffer run across the next schedule boundary. This prevents a late charge command from carrying into a Flow Power Happy Hour export window, and similarly keeps export/discharge commands from over-running their planned window.

**FoxESS optimizer timeout handling**
FoxESS optimizer commands now respect the exact optimizer duration instead of being stretched by PowerSync's previous 600-second remote-control minimum. Manual force commands keep the existing user-facing duration behavior, while optimizer-owned commands can follow the LP schedule precisely.

Update available via HACS
