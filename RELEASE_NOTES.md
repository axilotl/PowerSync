<!-- release: v2.12.345 -->

## What's Changed

**Fix mobile app energy statistics for Sigenergy and other non-Tesla systems**
PowerSync now builds calendar history for non-Tesla battery systems from Home Assistant recorder statistics for the daily solar, grid, battery, and home load sensors instead of returning only the current in-memory daily total. This gives the mobile app real period data for Solar, Grid, Battery, Home, and Load statistics when those values come from Sigenergy modbus or other PowerSync energy sensors.

**Keep today's in-progress totals current**
For the active day, PowerSync appends the live coordinator energy summary to the recorder-backed history so today's mobile app totals stay current while still using recorder data for completed periods.

Update available via HACS
