## What's Changed

**Octopus Energy: LP optimizer no longer skips the current half-hour when planning**
The optimizer's "drop past entries" filter was checking interval *start* time, which for any 30-minute tariff slot (Octopus AGILE/Cosy/Flux, Amber 30-min) silently dropped the *currently active* slot — its start time was always 0–30 minutes before "now". That left the LP reasoning with the *next* slot's price for the first ~10 minutes of every run, and on AGILE's wide spreads that flipped CHARGE/IDLE/EXPORT decisions on settlement boundaries. The filter now uses interval end time, and each surviving entry is expanded by its remaining minutes from "now" forward, so the LP sees the true price for the time it's actually planning over. Amber 30-min forecast users benefit too.

**Octopus Energy: Sigenergy & FoxESS Cloud time-of-use schedules no longer land 10 hours off in the UK**
The Sigenergy/FoxESS cloud TOU converter fell back to Australia/Sydney when no NEM region was configured. UK Octopus users with Sigenergy or FoxESS Cloud were getting their 6 PM peak prices bucketed into the 4 AM slot — the cloud schedule was effectively inverted, telling the battery to charge during peak and discharge overnight. The converter now accepts an explicit IANA timezone, and Octopus pushes Europe/London. Tesla Powerwall users were never affected (it derives its timezone from `site_info`).

**Octopus Energy + Sigenergy: cloud TOU upload no longer fights the LP optimizer**
When PowerSync's optimizer was active, the Sigenergy Cloud TOU sync was still uploading a competing schedule every 30 minutes. Sigenergy then tried to charge/discharge on the cloud plan while the LP issued conflicting Modbus commands, causing oscillation and unintended grid pulls. The cloud sync now skips upload whenever the LP is active (mirroring the existing FoxESS guard), so the LP has uncontested control over the inverter.

**Octopus Energy: BottlecapDave integration is now the source of truth for the active tariff**
PowerSync was using the Octopus product code typed into the config flow to decide whether to retrigger the LP on each price publish — but if BottlecapDave reported a different (or upgraded) tariff, the gate never matched and the LP only ran on its 5-minute periodic loop. The integration now promotes BottlecapDave's live `tariff_code` onto the price coordinator on every refresh, checks both product and tariff codes for AGILE/FLUX/COSY, and re-evaluates after each fetch — so a user who moves onto AGILE mid-session gets price-triggered re-optimization without restarting Home Assistant.

**Octopus Energy: block-rate tariffs (Go, Cosy off-peak) handled correctly when read from BottlecapDave**
The BottlecapDave reader hardcoded `duration: 30` on every rate, regardless of the actual interval width. If BottlecapDave emitted an unexpanded multi-hour block (which happens for some Go/Cosy off-peak windows), the LP saw it as a single 30-minute cheap slot instead of a multi-hour cheap window. The duration is now computed from the actual `start`/`end` timestamps so the LP plans against the correct slot length.

**Sigenergy plan label now reflects the actual provider**
Plans uploaded to Sigenergy Cloud were always labelled "PowerSync Amber" — confusing in the Sigenergy app for Octopus, AEMO, and Localvolts users. The label now matches the configured provider (e.g. "PowerSync Octopus").

Update available via HACS
