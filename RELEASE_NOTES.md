<!-- release: v2.12.736 -->

## What's Changed

**Optimizer force discharge now holds through short LP replans**
PowerSync now gives optimizer-owned force-discharge commands the same short minimum commitment used for force charging when the LP briefly replans to self-consumption while future export slots still remain. This prevents non-Tesla batteries from rapidly switching out of force discharge and back in during active export windows such as Flow Power Happy Hour.

**Export-window endings still cancel normally**
The hold only applies when the current schedule still contains a future export or discharge action inside the commitment window. When the export window has actually ended, PowerSync still cancels the optimizer-owned force discharge and restores normal battery operation.

Update available via HACS
