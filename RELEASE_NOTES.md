<!-- release: v2.12.440 -->

## What's Changed

**Smart Optimization returns to 5-minute cadence**
Smart Optimization now always runs on the fixed 5-minute interval again, including on installs that still had an older persisted optimizer interval saved. Runtime settings updates from the API or mobile app can no longer stretch the optimizer cadence back out to 30 minutes.

**Force modes restore on the current LP slot**
The optimizer no longer keeps a force charge or force discharge active just because a matching charge/export slot appears later in the short-term schedule. If the current LP slot changes back to self-consumption, PowerSync restores immediately and lets the next 5-minute optimization issue a fresh command if needed.

Update available via HACS
