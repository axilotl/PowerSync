<!-- release: v2.12.429 -->

## What's Changed

**Fixed long Intelligent Octopus Go charge windows**
PowerSync now prevents generic positive feed-in tariffs from turning cheap IOG import periods into battery export arbitrage loops. The optimizer can still charge from cheap import for later self-consumption, but it will not hold an all-day force charge window just because export is also positive.

**Charge sooner when sitting on the optimizer reserve**
When the battery is at the optimizer floor during a flat cheap window, LP tie-breaking now prefers charging at the start of the window instead of waiting until the last possible slots. This gives Powerwall and inverter force-charge commands time to engage and avoids low-SOC edge cases around off-peak windows.

Update available via HACS
