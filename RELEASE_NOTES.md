## What's Changed

Follow-up to the 2.11.13 Powerwall local-control release — fills in the parts phase 1 promised but didn't ship a UI for, plus the automatic re-pair detection that the signed transport was already surfacing internally.

**New: Configurable safety floors with sliders in Battery Setup**
Three new sliders in the mobile app give you direct control over when the integration will refuse an off-grid command. The **manual off-grid SOC floor** (in the Local Control card) sets the minimum battery level at which the Go Off-Grid button and the `power_sync.powerwall_go_off_grid` service will work — default 20%, range 5–90%. When the opt-in Off-Grid Curtailment toggle is on, two more sliders appear: a higher **curtailment minimum SOC** (default 40% — the session can run for hours, so we hold more headroom than the manual floor), and a **daily cap** in hours (default 6h) that resets at midnight and prevents a sticky negative-price trigger from draining the battery on repeat cycles. Sliders commit on release so you can drag smoothly without spamming the backend.

**New: "Detect on network" button in the pairing wizard**
The pairing wizard's Gateway Address step now has a **Detect on network** button that asks Home Assistant to query its live zeroconf cache for `_teslapowerwall._tcp` / `_teslanterstudio._tcp` advertisements. One match auto-fills the IP field. Multiple matches render as tap-to-select chips. No match tells you exactly what's going on: "No Powerwall found on the local network. Your router may block mDNS between subnets — enter the IP manually below." So users whose network plays nicely with mDNS get zero-friction pairing, and everyone else still gets clear guidance instead of a cryptic error.

**New: Push notifications on off-grid activation and release**
When the curtailment fallback automatically disconnects the Powerwall from the grid you now get a push notification explaining why, with the current SOC and the trigger reason humanised: *"⚡ Powerwall Off-Grid — Disconnected from grid to block excess export (negative export price). SOC 72%."* A matching notification fires on reconnect with the session duration: *"⚡ Powerwall Back On-Grid — Reconnected after 47m off-grid curtailment."* Best-effort, never blocks the state machine.

**New: Automatic re-pair detection**
If you revoke PowerSync's client key from the Tesla app, or factory-reset the gateway, the TEDAPI transport will start getting `UNKNOWN_KEY_ID` errors back from the Powerwall. The integration now catches those, flips the `binary_sensor.power_sync_powerwall_local_paired` sensor off, fires a *"🔒 Powerwall Re-pair Required"* push notification, and surfaces a yellow warning banner at the top of Battery Setup explaining what happened and prompting you to tap Pair Gateway to restore local control. No more silent failure when Tesla's side of the handshake changes underneath you.

**New: Off-grid automation actions now appear in the picker**
The two new automation action types — **Powerwall: Go Off-Grid** and **Powerwall: Reconnect to Grid** — now show up as chips in the Grid tab of the automation builder. They were in the type registry from the 2.11.12 release but the hardcoded category resolver never rendered them, which meant users literally couldn't add them to an automation from the UI. Fixed. The Python action dispatcher was already wired up — this was purely a missing chip.

**New: services.yaml entries for local off-grid services**
`power_sync.powerwall_go_off_grid` and `power_sync.powerwall_reconnect_grid` now have proper definitions in `services.yaml` so the HA Developer Tools → Services tab shows them with descriptions, a `bypass_soc_check` boolean selector for the rare "I know what I'm doing" manual override, and a pretty name. Previously they showed up but rendered with no description or field hints.

**Fix: Declared zeroconf as an after_dependency (hassfest)**
The new gateway discovery endpoint imports `homeassistant.components.zeroconf`, which hassfest validation requires to be declared in the manifest. Adding it to `after_dependencies` (not `dependencies`) keeps the integration loadable on the rare install that doesn't have zeroconf configured — the discover endpoint just returns an empty candidate list in that case, and manual IP entry still works. Caught by the HACS validation workflow and fixed in the 2.11.15 patch bump.

Update available via HACS
