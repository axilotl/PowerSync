## What's Changed

**Flow Power: Optimizer No Longer Exports at 0c**
The LP optimizer was scheduling battery exports during non-happy-hour periods when the Flow Power sell rate is 0c/kWh. It was treating 0c export as near-free, then planning to recharge from solar and export again during happy hour — but this still wastes energy through round-trip losses and unnecessary grid interaction. The optimizer now treats exporting at 0c as equivalent in cost to importing from the grid, so it will hold charge and wait for the 17:30–19:30 happy hour window instead.

Update available via HACS
