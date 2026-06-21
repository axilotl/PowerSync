<!-- release: v2.12.683 -->

## What's Changed

**Respect future-dated reserve bridge recommendations during export execution**
PowerSync now keeps future home-load bridge reserve floors scoped to their actual bridge date when executing forced export/discharge commands. This fixes a case where the optimiser could correctly plan a current-day export, but the executor would block it because tomorrow's recommended bridge reserve floor was applied early.

Update available via HACS
