<!-- release: v2.12.738 -->

## What's Changed

**Tesla outage alerts now require a sustained failure window**
PowerSync no longer treats a short burst of empty Tesla `live_status` responses as a full Tesla server outage just because several refresh attempts happen quickly. The outage notification now still requires repeated failures, but also waits for the failure streak to last about five minutes before pausing optimization and sending the outage alert.

Update available via HACS
