<!-- release: v2.12.584 -->

## What's Changed

**Dashboard now shows the Auto Reserve export floor**
The 24-hour optimiser card now displays a separate Export Floor chip and chart line when Auto Reserve calculates a higher export-only reserve for post-export home load. This makes it clear why an export window stops above the global Auto Reserve value instead of leaving the dashboard showing only 5%.

**Export floor diagnostics are preserved after the second solve**
Smart Optimization now carries the home-load export floor through the follow-up optimiser pass and exposes the applied export floor in the API payload. This keeps the dashboard, reserve recommendation, and planned export windows aligned after Auto Reserve recalculates.

Update available via HACS
