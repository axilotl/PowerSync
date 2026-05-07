<!-- release: v2.12.318 -->

## What's Changed

**Sigenergy tariff upload now sends distinct buy and sell schedules**
The Sigenergy cloud payload now keeps the canonical 30-minute import tariff in `buyPrice` and the canonical 30-minute feed-in tariff in `sellPrice` instead of mirroring import into both fields. This matches the Sigenergy tariff model while preserving the 48-slot, 30-minute schedule required by the app.

**Clearer Sigenergy upload diagnostics**
The Sigenergy sync log now reports both buy and sell period counts from the canonical conversion, making it easier to confirm the payload is 30-minute slots rather than the 5-minute optimizer interval.

Update available via HACS
