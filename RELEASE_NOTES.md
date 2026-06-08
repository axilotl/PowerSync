<!-- release: v2.12.610 -->

## What's Changed

**HA Dashboard EV control panel**
The generated PowerSync dashboard now includes a native EV charging panel with loadpoint status, quick Start/Stop/Boost controls, source-policy selection for Solar Only, Limited Grid + Solar, and Full Grid + Solar, and compact runtime controls for Solar Surplus, Price Level, Scheduled Charging, and Smart Schedule. The card uses the existing authenticated Home Assistant API endpoints, caches polling so unrelated HA state updates do not rebuild the card, and keeps charger setup details such as entity IDs, OCPP IDs, and mappings out of the dashboard.

**Dashboard EV source policies**
EV quick starts can now use a new `start_policy_charging` command behind the existing vehicle command API. Solar Only maps to manual solar-surplus dynamic charging, Limited Grid + Solar uses the existing battery-target dynamic defaults, and Full Grid + Solar uses the existing manual grid-allowed start path. Non-manual EV modes continue to own their loadpoints until stopped, so dashboard quick starts return a clear conflict instead of silently taking over an automated session.

**Flow Power KWatch API support**
Flow Power setup and options can now accept a KWatch API key, validate available residential sites, select the correct NMI, and prefill network tariff metadata when the API provides it. KWatch dispatch and predispatch prices are converted into PowerSync's existing tariff/forecast pipeline, and Flow Power account sensors can use KWatch summary data before falling back to the portal session path.

**Sigenergy EVDC charge-rate control**
Sigenergy EVDC chargers can now use a configured or auto-detected Home Assistant number entity for max charging power, allowing PowerSync to translate requested EV amps into a kW charge limit where the inverter exposes that control. Dynamic EV charging and solar-surplus sessions now advertise those EVDC capabilities consistently across mobile, widgets, loadpoint status, and charger actions.

**No Idle mode for supported TOU providers**
The optimizer's No Idle behavior is no longer hard-coded to Flow Power only. Supported TOU-style providers can expose the same option, while unsupported providers automatically coerce stale No Idle settings back off so optimizer settings do not persist an ineffective toggle.

Update available via HACS
