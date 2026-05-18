<!-- release: v2.12.427 -->

## What's Changed

**Fixed cheap overnight grid charging when export prices are higher than import**
PowerSync now distinguishes true battery-export profit windows from cheap import windows where the feed-in tariff is higher than the import price but still below the battery's stored-energy acquisition cost. Octopus Intelligent Go and similar tariff setups can now plan overnight grid charging when the battery is low instead of incorrectly treating those 7p import periods as export-only slots.

**Aligned greedy fallback with LP charging rules**
The optimizer fallback now uses the same acquisition-cost guard as the LP solver and chooses charging periods by cheapest import price, so systems without SciPy keep the same behavior around low overnight rates and positive feed-in tariffs.

Update available via HACS
