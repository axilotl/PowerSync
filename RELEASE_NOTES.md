## What's Changed

**Multi-currency support for international users**
PowerSync now adapts every price unit, sensor label, tariff payload, dashboard chart, and config-flow input to your provider's currency. Octopus accounts show GBP/p, EPEX shows EUR/ct, NZ retailers show NZD/c, and Australian providers (Amber, Flow Power, Globird, Localvolts, AEMO VPP) continue to use AUD/c. For generic "other" or custom-tariff setups, PowerSync follows your Home Assistant configured currency. Price gauges, the TOU schedule chart, the LP forecast chart, Flow Power TWAP and network tariff sensors, demand and supply charge sensors, daily import cost / export earnings, and every rate field across the setup and options flows all read the right unit automatically. The integration was originally built for the Australian market and hardcoded `$` and `c/kWh` in dozens of places — those are gone now.

**Tariff payloads carry currency metadata**
Generated and custom tariff schedules now include `currency`, `price_unit`, and `minor_price_unit` attributes so the mobile app, dashboards, and any downstream consumer can render the right symbol and formatting without guessing. Existing custom tariffs you've saved are upgraded transparently — they pick up the currency from your provider configuration the next time they're loaded, so nothing breaks for existing setups.

**TOU schedule chart now displays in cents instead of fractional dollars**
The dashboard's TOU schedule chart was reading `tariff_schedule` values in dollars per kWh but labelling the y-axis with "¢", so a 25c rate showed as "0.25¢" on the gauge. The chart now scales values by 100 to match the unit label, bringing it in line with the LP forecast price chart and showing prices the way you'd actually read them off your bill.

**Removed monetary device class from rate sensors to silence Home Assistant warnings**
Per-kWh price sensors (current import/export, LP price forecasts, AEMO wholesale price, average cost per kWh) were declaring `device_class: monetary`, which Home Assistant only supports when paired with `state_class: total`. The mismatch was producing repeated validation warnings in the log and could cause statistics anomalies. Rate sensors now use a plain unit-of-measurement and reserve the monetary device class for true monetary totals like daily costs and monthly supply charges, matching Home Assistant's stricter validation rules.

Update available via HACS
