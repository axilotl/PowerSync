## What's Changed

**Battery Health gauges now distinguish leader, expansion, and follower units**
The Home Assistant dashboard's Battery Health row used to label every non-follower slot as a generic "Battery N", so a typical Powerwall site with one leader plus two expansion packs and a follower showed up as "Battery 1 / Battery 2 / Battery 3 / Follower 4". The integration was already publishing per-slot `is_expansion` and `is_follower` attributes, but the dashboard only consulted the follower flag. Labels are now role-aware: gateway-attached units appear as **Leader N**, expansion packs hanging off a leader as **Expansion N**, and PW3-linked siblings as **Follower N** — making it obvious at a glance which unit is which when capacity numbers diverge.

Update available via HACS
