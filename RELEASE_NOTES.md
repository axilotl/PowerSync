## What's Changed

**Battery Health: Smarter ghost-expansion-pack detection**
The Tesla Fleet API occasionally returns BMS entries for expansion pack slots that are *registered* on the gateway but not *physically installed* — these phantom packs report plausible full-capacity numbers (13.5–14.5 kWh) but near-zero remaining energy regardless of system SOC, which inflated the reported battery count and skewed health calculations on affected sites. The previous filter treated every expansion-flagged pack as a ghost candidate and dropped them as a group, which mis-handled mixed installs that have both real and phantom expansion slots.

The filter now keys off the **serialNumber** field instead of the expansion flag alone. Real BMS modules — Main packs and physically-installed expansions — always populate a serialNumber. Phantom slots don't. The new heuristic identifies missing-serial expansions as ghost candidates, removes them from the count, and cross-validates by checking that the remaining packs' nominal-full-pack sum matches the system-level total within 10%. If the math agrees, the no-serial entries are dropped and `battery_count` / `rated_capacity` reflect only physically-installed packs. If the math doesn't match, no packs are filtered — better to over-report than to silently hide a real anomaly.

This corrects battery counts on sites with `1 Main + 1 real expansion + N phantom slots`, which the old filter would have collapsed to `1 Main` only.

Update available via HACS
