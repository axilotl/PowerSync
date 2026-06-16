<!-- release: v2.12.656 -->

## What's Changed

**Sungrow force charge keeps the inverter's charge limit available for solar**
PowerSync no longer lowers the Sungrow SH maximum battery charge register when starting an optimizer-controlled force charge. The requested force-charge power is still written to Sungrow's forced charge/discharge power register, but the inverter's broader charge ceiling is left unchanged so daytime solar can continue charging the battery above the grid-charge target instead of being pushed to export.

Update available via HACS
