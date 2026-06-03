<!-- release: v2.12.559 -->

## What's Changed

**Fix: unreachable Powerwall could crash-loop Home Assistant**
If your local Powerwall gateway became unreachable (network change, VLAN/routing issue, gateway offline), PowerSync's local poll could hang for ~100 seconds instead of failing quickly. During Home Assistant startup that long stall could blow past HA's setup window and fail the integration, which on low-power hardware (like HA Green) showed up as Home Assistant restarting over and over. PowerSync now fails fast and degrades gracefully: every local poll is capped at 15 seconds, the network connect is bounded to ~5 seconds, and the local warm-up runs in the background so a slow or offline gateway can never stall startup. The Powerwall entities simply show unavailable and recover on their own once the gateway is reachable again.

**Faster optimiser after a restart**
The optimiser's first schedule was held back by a fixed 90-second timer after every restart, so it took unnecessarily long to start acting. That hold now tracks when Home Assistant has actually finished starting, so the first optimisation runs as soon as startup settles — typically much sooner — instead of waiting out a fixed timer. This pairs with the recent move of the optimiser's heavy first-run data crunching off the main loop, so startups are smoother and the optimiser gets to work faster.

Update available via HACS
