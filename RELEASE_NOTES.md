<!-- release: v2.12.557 -->

## What's Changed

**Battery no longer drains to 5% when the optimiser can't find a plan**
When Smart Optimization couldn't solve its schedule (an "infeasible" forecast — e.g. an already-low battery combined with a tight reserve target), it used to quietly drop your backup reserve to 5% and re-solve, which let it discharge the battery almost flat overnight. It now holds in self-consumption instead: the battery only serves your home load, never exports to the grid, never charges from the grid, and never drops below your real reserve. If it's already below reserve it holds rather than draining further. This self-heals on the next solve once a valid plan is available.

**Much faster Home Assistant startup**
Smart Optimization now uses the HiGHS solver directly (via highspy) instead of SciPy. SciPy was one of the heaviest Python packages PowerSync pulled in — slow to install on updates and several seconds to load on every restart. HiGHS is far lighter and ships ready-built for Home Assistant OS, so startups are quicker and updates install faster. The optimisation maths is unchanged — schedules are identical to before — and PowerSync still falls back to its simple built-in optimiser if the solver isn't available.

**Fresher tariff after a restart**
The first price/tariff sync after a restart used to be held back by a fixed 90-second delay, leaving your battery on a stale tariff for up to a minute and a half after every reboot. That delay now tracks when Home Assistant has actually finished starting, so the sync happens as soon as startup is done — typically just a few seconds — instead of waiting out an arbitrary timer.

Update available via HACS
