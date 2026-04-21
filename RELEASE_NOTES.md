## What's Changed

**Dashboard: Force Power Slider Now Renders Correctly**
The Force Power slider on the HA dashboard was showing a raw JavaScript template string as its title and rendering as an empty dark bar. Switched from a tile card (which doesn't evaluate button-card templates) to a standard entities card, which natively renders number entities as sliders. The label now reads "Force Power (0 = Max)" making it clear that leaving it at 0 uses the inverter's full rated power.

Update available via HACS
