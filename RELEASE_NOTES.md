<!-- release: v2.12.651 -->

## What's Changed

**Restore Tesla grid charging to its pre-force state**
PowerSync now records whether Tesla grid charging was enabled or disabled before manual force charge or force discharge starts, and restores that same state when normal operation resumes. This prevents a force charge from leaving Powerwall grid charging enabled when it was previously off, while still preserving the existing demand-period protection and optimizer handoff behavior.

Update available via HACS
