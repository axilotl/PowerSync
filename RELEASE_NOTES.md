<!-- release: v2.12.451 -->

## What's Changed

**Fix mobile energy detail totals for non-Tesla systems**
Calendar history rows for FoxESS, Sungrow, and other energy-summary based systems now include the Tesla-style detail fields that the mobile app still reads on its Solar, Grid, Home, and Battery detail screens. This keeps the existing normalized fields while adding compatible solar, grid, battery, and home-consumption aliases so Android no longer shows 0 Wh when Home Assistant has live daily energy data.

Update available via HACS
