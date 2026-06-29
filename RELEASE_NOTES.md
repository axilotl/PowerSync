<!-- release: v2.12.737 -->

## What's Changed

**Robust historical load forecast scaling**
PowerSync now ignores short high-load spikes when deciding whether recent household usage has shifted enough to scale the historical load forecast. This prevents brief EV charging sessions from inflating every future load bucket and causing the optimizer to plan around phantom load outside the normal charging window.

Update available via HACS
