<!-- release: v2.12.531 -->

## What's Changed

**Smoother static export windows**
PowerSync now keeps optimiser-controlled export mode active through a single 5-minute self-consumption island when the surrounding static-tariff export slots have the same export price. This avoids unnecessary stop-and-restart mode churn at export window transitions, so systems do not briefly drop back to self-consumption only to re-enter export on the next optimiser interval.

**Dynamic pricing guardrails**
The smoothing is deliberately disabled for Amber and AEMO dynamic pricing, and it also refuses to bridge a gap when the skipped slot has a different export price or pricing data is unavailable. Legitimate one-slot price dips therefore remain real optimiser decisions rather than being flattened away.

Update available via HACS
