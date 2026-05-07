<!-- release: v2.12.326 -->

## What's Changed

**Fix NeoVolta dual-inverter house load**
PowerSync now derives combined NeoVolta house load from the fleet power balance instead of trusting a gross per-inverter house-load sensor. This fixes dual-inverter AC-coupled sites showing inflated home load, such as a 6 kW load when the real site balance is around 1.3 kW.

**Hide empty PV string details on AC-coupled systems**
The dashboard now only shows PV String Details when real PV string power or current is present. AC-coupled NeoVolta systems with zero string power and tiny disconnected string voltages no longer display an irrelevant string-details card.

**Clarify Auto-Sync naming for Modbus batteries**
Non-Tesla systems now show Auto-Sync Tariff Prices instead of Auto-Sync TOU Schedule, and the service wording explains that Tesla uploads a schedule while Modbus systems store tariff data for PowerSync display and optimization.

Update available via HACS
