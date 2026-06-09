<!-- release: v2.12.613 -->

## What's Changed

**Flow Power KWatch setup accepts price-only API keys**
Flow Power KWatch setup and options now validate API keys against the dispatch and predispatch pricing endpoints when the residential-site lookup is unavailable. This lets users whose NMI is not linked in the KWatch portal still use KWatch pricing instead of being blocked by a misleading provider-portal connection error.

**KWatch account metadata lookup is optional**
Runtime account refresh now treats unavailable KWatch residential-site metadata as optional, so pricing can continue quietly without repeated warnings when only the price endpoints are available.

Update available via HACS
