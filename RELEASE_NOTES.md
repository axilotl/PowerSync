<!-- release: v2.12.327 -->

## What's Changed

**Preserve dual NeoVolta inverter baseline modes**
PowerSync now remembers each NeoVolta inverter's stable dispatch mode before taking control and restores those per-inverter modes afterward. This supports dual-inverter systems without a parallel kit where one inverter may need to stay in Idle while the other runs Normal to avoid battery-to-battery circulation losses.

**Stop stale custom dashboard layouts from causing render loops**
The custom PowerSync dashboard layout now validates saved browser layouts before applying them. If the saved card order is stale, duplicated, or no longer matches the current dashboard cards, PowerSync clears that saved layout and falls back to the default instead of repeatedly reflowing charts and the power-flow card.

Update available via HACS
