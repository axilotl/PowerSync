<!-- release: v2.12.305 -->

## What's Changed

**Sigenergy tariff display fix**
Sigenergy cloud tariff sync now mirrors the Amber import schedule into the cloud sell-price payload instead of uploading Amber feed-in prices as a second visible tariff schedule. This prevents the Sigenergy app from showing the lower feed-in figures after the correct import tariff has been generated, while PowerSync continues to use the live provider prices directly for optimization and export decisions.

Update available via HACS
