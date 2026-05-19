<!-- release: v2.12.438 -->

## What's Changed

**Spread Smart Optimization imports across same-price windows**
PowerSync now has an optional Spread Import Across Window setting for supported non-Tesla battery systems. When Smart Optimization plans grid charging inside a fixed-price or free import window, it keeps the optimiser's chosen energy target but spreads that charge across the whole same-price window instead of charging at maximum power immediately.

**Smarter free-power charging near full batteries**
For zero or negative import windows, spread import mode now accounts for the battery room available at the start of the window. This avoids over-requesting max charge when the battery is already close to full and lets free-power charging taper across the available window.

**Powerwall off-grid fallback option for export curtailment**
Tesla Powerwall users now get an optional off-grid fallback in curtailment settings. When enabled, PowerSync can temporarily island the Powerwall for export curtailment if no AC inverter curtailment path is configured or available.

Update available via HACS
