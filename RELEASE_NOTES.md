<!-- release: v2.12.658 -->

## What's Changed

**Fix mobile energy graphs when Home Assistant statistics are missing**
PowerSync now falls back to Home Assistant recorder state history for non-Tesla mobile calendar graphs when compiled long-term statistics are not available yet. This lets FoxESS and other daily-energy systems return hourly/day energy rows instead of a single cumulative point that can make the mobile app graph appear as one large spike.

Update available via HACS
