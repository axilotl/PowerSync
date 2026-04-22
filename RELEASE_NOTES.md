## What's Changed

**Battery Health: Correct Capacity and Pack Count for Multi-Unit Systems**
Systems with a PW3 leader + follower were showing wrong battery count, rated capacity, and overall health because the per-pack sum from `components.msa` was overriding the authoritative `control.systemStatus` total — but only the leader's expansion packs were reporting BMS energy signals, leaving the follower out of the count. The fix stops overriding the systemStatus aggregate (which always covers all units) and uses the highest module count seen across both `batteryBlocks` and per-pack BMS entries. Debug logging now dumps the full msa component list to help diagnose missing entries.

Update available via HACS
