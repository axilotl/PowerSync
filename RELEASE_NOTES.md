## What's Changed

**Away Mode Redesign — Enable Before Leaving**

Away Mode has been completely redesigned to match the intuitive mental model. Previously, enabling the switch skipped the last 7 days of load history — only useful *after* returning, and confusing to use. Now, enable Away Mode *before* you leave: the LP continues using normal recent history while the house is empty, so vacation-low load data naturally accumulates and biases it toward exporting rather than reserving charge for non-existent consumption. When you get home, turn it off — this starts a 7-day recovery window that excludes the vacation period from the load history and backfills with your pre-departure patterns instead. As each new day of real post-return usage accumulates, it slots in and gradually replaces the backfill. After 7 days, the window closes automatically. State persists across HA restarts, and short toggles under an hour are treated as no-ops to avoid corrupting the history.

**Profit Maximisation Mode (switch.power_sync_profit_maximisation_mode)**

A new switch for users on dynamic tariffs (Flow Power, Amber, Octopus Agile) who want the LP to export more aggressively during peak export windows like Flow Power's 45c/kWh Happy Hour. When enabled, the LP's *terminal valuation* drops to 30% of its normal value — it stops reserving as much charge for post-horizon needs — and the confidence decay trust horizon extends from 6h to 12h, so far-future export spikes are factored in earlier in the day. The trade-off: you'll capture more export revenue on good days, but if solar underperforms or overnight prices spike, you may import more from the grid than the conservative default would have required. Appears in Settings → Devices & Services → PowerSync → Configuration.

Update available via HACS
