<!-- release: v2.12.538 -->

## What's Changed

**Auto-Apply Optimizer Reserve now tracks back down**
PowerSync now calculates the next auto-applied optimizer reserve from the saved manual reserve baseline instead of the already-applied live optimizer floor. This prevents a high calculated reserve, including 100%, from feeding back into the next solve and getting stuck there. The final dispatch schedule is still re-solved with the active applied reserve.

**Calculated optimizer reserve on the schedule graph**
The Home Assistant Smart Optimization schedule graph now labels the applied auto reserve as `Calculated Reserve` and shows an `Auto Reserve` chip while auto-apply is enabled. When auto-apply is off, the graph continues to show the normal optimizer reserve floor.

Update available via HACS
