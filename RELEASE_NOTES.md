## What's Changed

**Dashboard: Battery Health Now Shows All Units in Stacked Powerwall Systems**
The Battery Health card previously showed a hardcoded grid of three individual battery gauges. It now reads the battery count from the entity's state at render time and generates the correct number of gauges automatically, up to eight. Follower units (the stacked expansion packs in multi-gateway Powerwall 3 setups) are now labelled "Follower N" rather than "Battery N" so it's immediately clear which readings are inferred from the aggregate versus directly measured. A note appears beneath the capacity line whenever follower units are present.

Update available via HACS
