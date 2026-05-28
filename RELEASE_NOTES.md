<!-- release: v2.12.493 -->

## What's Changed

**Smart Schedule respects the real site import limit**
EV Smart Schedule now resolves the maximum grid import limit from Tesla's site meter setting when a paired Powerwall exposes it, including `max_site_meter_power_ac`. If Tesla does not provide a value, PowerSync falls back to the Home Power main breaker setting and then the existing default. This lets EV charging use available headroom during cheap or free periods while still respecting the site's configured import cap.

**Battery target charging now handles Powerwall tapering**
Cheap and free grid charging windows now pass the optimizer's battery charge target into the dynamic EV controller. When the Powerwall is nearly full and naturally tapers its charge rate, PowerSync treats the unused site import capacity as EV headroom instead of holding the EV below the available limit.

**Home Power setup can store breaker-based fallback limits**
The Home Power API now stores main breaker size and default voltage so non-Tesla systems, unpaired Powerwalls, or sites without Tesla's meter limit can still configure a site import cap for dynamic EV charging.

Update available via HACS
