## What's Changed

**Custom TOU / AEMO spike config now available beyond Globird**
The optional AEMO price-spike export and custom tariff settings page used to only appear for users on the Globird and AEMO VPP providers. It's been renamed to "Custom TOU / AEMO settings" and is now also reachable when your electricity provider is set to `other` or `tou_only`, so anyone running a flat or fixed TOU plan can opt in to AEMO spike exports without having to misrepresent their retailer. The OptionsFlow also sets `_provider` defensively so saving the page no longer crashes if the flow's internal state was missing the field.

**Calendar history works on more battery brands**
The mobile app's calendar/history endpoint previously had separately copy-pasted blocks for each supported inverter, with AlphaESS and ESY Sunhome missing entirely. The endpoint now resolves the energy-summary coordinator generically and supports Sigenergy, Sungrow, FoxESS, GoodWe, AlphaESS, ESY Sunhome, Solax and SAJ H2 from one shared code path. AlphaESS and ESY Sunhome users get history + cost summary for the first time, and the others get the same behaviour as before with less risk of inverter-specific bugs.

**Dashboard strategy detects more HACS resources correctly**
The dashboard strategy checks whether each frontend card (button-card, apexcharts-card, etc.) is registered as a Lovelace resource. The match was case-sensitive and only compared against the JS element name with hyphens removed, which missed resources whose URL used the HACS package name or different casing. The strategy now compares against both the element name and the HACS package name, with hyphen variants and case-insensitive matching, so HACS-installed cards that previously appeared "missing" are recognised.

Update available via HACS
