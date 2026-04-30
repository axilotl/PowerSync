## What's Changed

**SAJ H2 force discharge now pushes to grid at full rate**
Reworked `force_discharge` to use TOU mode with a dedicated slot 7 (00:00–23:59 at 100 % rated power) instead of passive mode. Passive discharge is load-following with only a small grid-push margin, so it could not export at AEMO spike rates — TOU mode adds PV on top of the configured target and dumps the battery's full rated discharge to grid, exactly what's needed for spike windows. Charge slots are temporarily cleared on entry and restored on exit so user-configured charging doesn't fight the discharge. PowerSync owns slot 7 only — slots 1–6 stay yours.

**SAJ H2 inverter rated power is now a config field**
Added an "Inverter rated AC power" field in SAJ H2 setup (read off the model number — e.g. HS2-10K-T2-5 → 10 kW). The LP-requested watts are encoded as `% × 10` of rated power for the SAJ registers, and the previous logic was reading a percentage as if it were watts and feeding the LP wrong charge/discharge limits. The cap is now 1000 (= 100 % of rated); the old 1100 sentinel is no longer written because it was triggering load-following fall-back on current firmware instead of true rated discharge.

**Powerwall local gateway login no longer spams 401s**
The local Powerwall client was hammering `/api/login/Basic` every poll cycle and producing endless `v1r login failed (401)` warnings whenever credentials were wrong, missing, or rate-limited. Login is now serialised behind a lock, the token is cleared on 401/403 so the client retries cleanly, and a 429 from the gateway triggers an exponential backoff (60 s → 300 s max, respects `Retry-After`) so failed credentials no longer flood the log or the gateway.

**Powerwall local pairing now collects the customer password**
The initial setup and options flow now expose a "Powerwall customer password" field alongside the gateway IP — usually the last 5 characters of the gateway serial/DIN (not your home Wi-Fi password). The IP and password are validated together: setting one without the other is rejected up front instead of failing silently at runtime. The mobile-app `set_gateway_ip` endpoint accepts the password too so you can finish local setup from the app without re-pairing.

**LP price forecast chart shows real export rates**
The LP Forecast price chart was clamping the Export series to 0 during midday oversupply periods, which made hours-long stretches look like flat zero whether the network was paying you nothing or charging you to export. The display now stores the signed rate (negative when you'd pay to export) while the LP optimiser still sees the clamped value, so the chart's green Export line dips below zero during real negative-feed-in windows and stays informative. Cost tracking and predicted-cost projections also use the signed value, correctly accounting for any export that does happen during paying-to-export periods.

Update available via HACS
