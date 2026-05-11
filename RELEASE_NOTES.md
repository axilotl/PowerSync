<!-- release: v2.12.383 -->

## What's Changed

**Keep Tesla optimizer force export active for the full planned window**
PowerSync now tracks the Tesla force-tariff window separately from the optimizer's software countdown. When Smart Optimization keeps an export or force-charge window open past the original Tesla TOU tariff window, PowerSync refreshes the uploaded tariff instead of only extending the internal state, preventing the dashboard from showing export while the Powerwall has already fallen back to normal import behavior.

**Improved Tesla force-mode recovery across restarts**
Force charge and discharge state now persists the hardware tariff expiry as well as the visible countdown, so restarted systems can avoid stale optimizer force windows and re-evaluate the correct hardware state.

Update available via HACS
