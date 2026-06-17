<!-- release: v2.12.670 -->

## What's Changed

**FoxESS Cloud: keep the last battery level when the cloud drops SoC**
When PowerSync runs FoxESS through the cloud, the FoxESS Open API realtime feed occasionally returns a sample without the battery state-of-charge value. PowerSync was treating that as 0%, which made the optimiser think the battery was empty and fall back to idle even with plenty of charge left. PowerSync now keeps the previous battery level when the cloud omits SoC, and only reports 0% when the inverter genuinely reports 0% — matching the existing Sungrow and Sigenergy behaviour.

Update available via HACS
