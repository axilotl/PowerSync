## What's Changed

**Tesla Energy and Tesla EV API providers are now configured separately**
The "Tesla API Provider" setting has been split into two independent dropdowns: **Tesla Energy API Provider** (PowerSync.cc / Tesla Fleet API / Teslemetry) for Powerwall control, and **Tesla EV API Provider** (None / Tesla Fleet API / Teslemetry) for vehicle commands. The PowerSync.cc free proxy doesn't expose vehicle endpoints, so users on PowerSync can now pair it with Tesla Fleet or Teslemetry purely for vehicle control without giving up the free Powerwall path.

**Detection of installed Tesla integrations**
The new EV provider dropdown automatically detects whether the `tesla_fleet` or `teslemetry` HA integrations are loaded and labels each option with a ✓ tick when found. If you pick Tesla Fleet without it being installed, you'll get a clear error pointing you to install it first. If you pick Teslemetry without it being installed, PowerSync prompts for an API token directly so vehicle commands work without needing the Teslemetry HA integration at all.

**Identical EV provider UX in both initial setup and options**
Both the first-time setup wizard and the post-install options flow now show the same Tesla Energy + Tesla EV provider dropdowns, validation, and Teslemetry token entry follow-up. Switching providers later works exactly the same as picking them on day one.

**Migration: existing installs keep working unchanged**
On upgrade, the Tesla EV provider defaults are derived from your existing energy provider — Tesla Fleet/Teslemetry users keep using the same source for vehicles, and PowerSync.cc users default to "None" until they explicitly opt in. Nothing breaks; the new setting only takes effect after you visit the options page.

**Fix: Minimum Discharge Level no longer shows a confusing checkbox**
The "Minimum Discharge Level (%)" field across all battery system setups (Tesla, Sigenergy, Sungrow, FoxESS, GoodWe) was rendered with an "enable this field" checkbox because it was marked as an optional schema field. The slider is now always shown without the checkbox, removing a UI surprise that suggested the level itself could be turned off.

**New Tesla Energy Site dashboard section**
The auto-generated PowerSync dashboard now includes a "Tesla Energy Site" entities card grouping all the controls added in v2.10.0 — backup reserve, operation mode, grid export rule, grid charging, manual export override, and (where the site supports them) storm watch, off-grid EV reserve, and per-program VPP enrollment switches. The card uses a domain-aware entity finder so it works regardless of the device-name prefix HA chose for your installation.

Update available via HACS
