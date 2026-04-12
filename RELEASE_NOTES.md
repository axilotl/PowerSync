## What's Changed

**Fix: Gateway mDNS "Detect on network" works on modern HA**
The new gateway discovery endpoint was crashing with `'HaZeroconf' object has no attribute 'zeroconf'` and returning an empty candidate list regardless of what was actually on the LAN. Home Assistant 2025+ returns the `HaZeroconf` instance from `async_get_instance()` directly — earlier releases wrapped it in an `AsyncZeroconf` which is where my old `.zeroconf` accessor came from, and using it on the modern API raises `AttributeError`. The discover endpoint now calls the `HaZeroconf` instance directly, pulls cached service names for `_teslapowerwall._tcp` / `_teslanterstudio._tcp` out of the live browser cache, and resolves each one into `ServiceInfo` records with a short timeout. Users whose routers let mDNS across subnets will now see their gateway auto-detected when they tap "Detect on network" in the pairing wizard.

Update available via HACS
