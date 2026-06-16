<!-- release: v2.12.659 -->

## What's Changed

**Fix duplicate daily energy buckets in mobile graphs**
PowerSync now ignores same-day transient drops in recorder fallback history for cumulative daily energy sensors. This prevents Home Assistant restart or restore states from making FoxESS and other non-Tesla mobile energy graphs count the same daily total multiple times, which could show inflated battery, solar, grid, or home usage values after the v2.12.658 fallback started using recorder state history.

Update available via HACS
