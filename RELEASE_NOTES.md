## What's Changed

**Calendar history now works on Sigenergy systems**
The mobile app's calendar/history view previously returned an error on Sigenergy installs because the integration explicitly blocked the endpoint for that brand. The endpoint now returns today's coordinator totals — solar generation, battery charge/discharge, grid import/export and home consumption — along with a cost summary derived from your tariff schedule, so Sigenergy users finally see their daily energy breakdown in the app.

**Profit Maximisation toggle stays in sync with the mobile app**
Toggling Profit Maximisation mode from the mobile app (or any other API caller) now updates the corresponding Home Assistant switch immediately, instead of leaving it stuck at the last value until a restart. The optimisation settings API accepts a new `profit_max_enabled` field, and a dispatcher signal pushes the new state straight to the `Profit Maximisation Mode` switch — which now also reads its live state from the coordinator, so external changes never desync. A `_skip_reload` guard prevents the config entry from restarting on every toggle.

Update available via HACS
