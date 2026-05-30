<!-- release: v2.12.512 -->

## What's Changed

**Open-Meteo Solar Forecast support**
PowerSync can now use the Open-Meteo Solar Forecast Home Assistant integration as a solar forecast source for Smart Optimization. Solcast remains supported, but Open-Meteo is now auto-detected and its `watts` forecast data is converted into the optimizer's 5-minute solar forecast inputs. Multiple Open-Meteo forecast entries are combined, which helps multi-array systems avoid Solcast free-tier limits.

**Solar forecast setup text**
Weather and solar forecast settings, warnings, the README, and wiki guidance now describe Solcast and Open-Meteo Solar Forecast as supported forecast providers instead of treating Solcast as the only option.

**Calendar history current-day totals**
Calendar history now keeps day-level statistic queries through the requested end time, and appends only the residual live total when recorder rows already cover part of the current day. This prevents duplicated current-day energy totals while preserving up-to-date daily views.

**Tesla backup reserve handling**
Smart Optimization now treats a manually raised Tesla backup reserve as the current hardware reserve when it is above the cached optimizer target and still below current SOC, instead of immediately forcing it back down during self-consumption.

Update available via HACS
