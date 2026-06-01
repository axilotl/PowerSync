<!-- release: v2.12.534 -->

## What's Changed

**Smart Optimization maximum grid import limit**
Smart Optimization now has a separate Maximum grid import setting for the site import ceiling. This keeps the real battery charge limit intact while the planner caps total grid import, so solar can still lift charging above the grid-only headroom without overestimating what the site can import during free or cheap windows.

**More accurate capped charging plans**
The optimizer now applies the site import cap across LP, fallback, pre-window target, and spread-import calculations. Charge plans account for forecast load and solar when deciding the feasible battery charge rate, which avoids unreachable SOC targets when household load consumes part of the grid allowance.

Update available via HACS
