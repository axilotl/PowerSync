<!-- release: v2.12.463 -->

## What's Changed

**Built-in load forecasting only**
PowerSync no longer checks for HAFO/HAEO or reads HAFO forecast sensors. Smart Optimization now forecasts household load from Home Assistant recorder history first, then uses the simple residential fallback when history is unavailable. This removes the stale external forecast/optimizer path and keeps the decision model inside PowerSync.

**Smarter 30-day history model**
The local load model now uses a 30-day history window with 14-day recency weighting, outlier clipping, same weekday/weekend fallback, single-sample blending, and the existing smoothing pass. Away Mode exclusion and optional weather temperature fitting now use the same filtered load-history window.

**Safer optimizer startup cleanup**
When Home Assistant restarts while an optimizer force mode is stale, PowerSync clears that state without issuing a new self-consumption command and waits for cleanup before running the next optimization solve. That avoids extending stale force behavior during startup.

Update available via HACS
