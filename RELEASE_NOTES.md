## What's Changed

**Price-Level charging now works for unsupported EVs**
Previously, Price-Level charging refused to start any charger that PowerSync couldn't read a battery level from (most generic OCPP setups, including the Sigen EVAC). Setting Recovery Charge to 0% with both price thresholds at the same value should have charged purely off the grid price, but the executor returned "Could not get EV state of charge" and never sent a start command. Now, when the EV's SOC is unknown, Recovery mode is skipped and the decision falls through to the Opportunity-price gate — so charging starts whenever the grid price is at or below your configured threshold, regardless of whether PowerSync can see the car's battery.

**OCPP charging sessions are now recorded automatically**
Sessions on OCPP chargers (HACS lbbrhzn/ocpp) weren't appearing in the app's charging history because PowerSync only logged sessions it kicked off itself — anything started from Home Assistant, RFID, the charger button, or even the app's own Start button was invisible. A new 30-second poll watches every detected OCPP charger's connector status and power meter, opening a session the moment the connector enters "Charging" and closing it when the connector becomes available again. Cost, power, and energy are tracked per-tick using the same Amber/tariff data the Zaptec poll already uses, so manual and price-level sessions both show up in history with full attribution.

**OCPP charger can be restarted after a stop**
Stopping an OCPP charger leaves the connector in "Finishing" state until the cable is unplugged. In that state, the HACS OCPP `charge_control` switch latches its `is_on` and silently swallows the next start command, so PowerSync (and the app's Start button) couldn't restart charging — the only workaround was toggling the switch from the HA dashboard. The OCPP start path now detects this state, briefly toggles the switch off and back on to force a fresh `RemoteStartTransaction`, and logs that the reset happened. Restarting from the app or from price-level charging now works without manual intervention.

Update available via HACS
