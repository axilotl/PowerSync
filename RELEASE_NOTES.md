<!-- release: v2.12.544 -->

## What's Changed

**Optimizer SOC chart reserve floor**
The Smart Optimization schedule now keeps the displayed SOC line above the effective reserve floor. This fixes cases where the backend schedule could draw the forecast SOC down to 0% during self-consumption even though the battery hardware reserve or optimiser reserve would prevent that in practice.

**Clearer reserve behavior below optimiser reserve**
When live SOC is already below the configured optimiser reserve, the schedule display now follows the same hardware-floor behavior used by the optimiser. This keeps Profit Max, Auto-Apply Optimizer Reserve, and self-consumption plans visually aligned with what PowerSync will actually execute.

Update available via HACS
