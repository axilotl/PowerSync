## What's Changed

**Battery Health: Individual Pack Capacity and Energy Now Show Correct Values**
The per-pack BMS signals from the Tesla Fleet API report energy in kWh, but the app expects Wh — so values like 14.38 kWh were being passed through as-is and displayed as 0.01 kWh, with Health vs Rated showing 0.1% instead of ~106%. The fix multiplies pack energy values by 1000 before sending them to the app, so Full Capacity now shows ~13.5–14.5 kWh per pack with correct health percentages. This fix was intended for v2.12.126 but wasn't included in that release.

**Battery Health: Follower PW3 Correctly Labelled**
The follower PW3 base module was being labelled "Expansion 3" in the Individual Packs list. It's now identified and labelled "Follower Unit" — detected by the presence of BMS signal keys with no energy data (the follower's BMS telemetry isn't reported individually by the Tesla API).

Update available via HACS
