## What's Changed

**New: Auto-detect the Gateway serial so you don't have to look it up**
Tesla's Fleet API `site_info` response contains the Gateway DIN in the format `{part_number}--{serial_number}` — the customer password the Powerwall's REST login endpoint expects is literally the last 5 characters of that serial. Rather than asking users to crawl under their Powerwall and read a sticker, the integration now parses the DIN from the site_info cache (or fetches fresh if the cache is empty), extracts the serial number, and exposes both the full serial and the suggested 5-character customer password via a new endpoint. The mobile pairing wizard calls this on focus and pre-fills the customer password field automatically — you can still override it, but in 99% of cases you won't have to touch it. Works on Powerwall 2 (Backup Gateway serial) and Powerwall 3 (PW3 unit serial, since the PW3 integrates gateway functionality).

Update available via HACS
