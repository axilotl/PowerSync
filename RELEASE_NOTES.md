<!-- release: v2.12.726 -->

## What's Changed

**Hold optimizer force charge through short LP flips**
PowerSync now keeps optimizer-owned non-Tesla force charge active for a minimum commitment window when a noisy solar nowcast briefly makes the LP switch the current slot back to self-consumption or idle. This prevents repeated charge/cancel command churn on overcast mornings where live solar swings around the boundary of whether the battery will reach the target before a later export window.

**Preserve the original charge commitment start**
Hardware refreshes for an active optimizer force charge now preserve the original start time, so the commitment window remains bounded and still hands back to normal operation after the window if the plan no longer wants charge.

Update available via HACS
