## What's Changed

**Time-of-use sync is now AEMO-dispatch-driven (1 POST per 5 min)**
PowerSync's 4-stage tariff sync used to fire up to three Tesla updates per 5-minute period — an initial forecast at :00, plus REST-API rechecks at :35 and :01 of the next minute. Analysis of recent logs showed this was producing ~42% more Tesla API calls than necessary, with Stage 3 firing *just before* AEMO publishes settled prices and Stage 4 firing right after. The integration now subscribes to AEMO's new-dispatch event and runs exactly one tariff sync per 5-minute period, automatically aligned with the moment AEMO publishes the settled price (typically +36–43 s after each boundary). Result: one Tesla call per period, always against the freshly settled price, never against the forecast. This applies to Amber, Flow Power, AEMO sensor, and Localvolts. Octopus UK isn't on NEM and gets its own single cron at :00 and :30. GloBird and AEMO VPP are unaffected (they don't sync TOU). Manual force charge / force discharge are unchanged — they still go through immediately, regardless of when the periodic sync last ran.

**"Settled Prices Only" option removed**
The "Settled Prices Only" toggle in Amber Settings has been removed. Settled-only behavior is now the default and only behavior whenever automatic TOU sync is enabled — the option no longer exists because there's nothing to choose between. Existing entries with the flag set will continue to work; the value is simply ignored. The matching toggle has also been removed from the mobile app (build 345+).

**Correct API provider name in tariff sync logs**
TOU sync log lines previously hard-coded "Teslemetry API" regardless of which Tesla API the user was actually configured for. They now show the real provider name (`powersync`, `fleet_api`, or `teslemetry`), making it possible to tell from the log which path a tariff POST took. Affected log lines: the per-attempt sync log, the network error log, and the timeout log inside `send_tariff_to_tesla`.

Update available via HACS
