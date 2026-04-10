## What's Changed

This release re-announces the work shipped in 2.10.0 and 2.11.0 — both were significant updates but the Discord notification on those releases came through with empty release notes due to a workflow ordering bug (now fixed). Below is the full picture of everything added in the last two releases plus this fix.

---

### 2.11.0 — Tesla Energy + Tesla EV API providers split

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
The auto-generated PowerSync dashboard now includes a "Tesla Energy Site" entities card grouping all the controls added in 2.10.0 — backup reserve, operation mode, grid export rule, grid charging, manual export override, and (where the site supports them) storm watch, off-grid EV reserve, and per-program VPP enrollment switches. The card uses a domain-aware entity finder so it works regardless of the device-name prefix HA chose for your installation.

---

### 2.10.0 — Tesla Energy Site capability surface

**Tesla Energy Site capability probe**
On first connection PowerSync now probes the Tesla Fleet API to detect which energy-site features your specific Powerwall installation actually supports — Storm Watch, off-grid EV reserve, and VPP/grid-services programs. Unsupported features (e.g. VPP programs outside the US) simply don't appear in HA or the mobile app, so you only ever see controls that actually work for your site.

**Storm Watch control**
A new switch entity lets you enable or disable Tesla's predictive pre-charging before severe weather, alongside a binary sensor that tells you when Tesla is currently treating an event as imminent. Both are also surfaced in the mobile app's Controls screen and as a new automation action and weather trigger condition.

**Off-grid EV charging reserve**
You can now set a separate battery reserve percentage that Tesla holds back specifically for vehicle charging during a grid outage, via a new number entity, the mobile app Controls screen, and the new `set_off_grid_ev_reserve` service and automation action. This is independent of the regular backup reserve.

**Tesla VPP / grid-services enrollment**
For sites that are eligible (typically US Tesla Electric / VPP customers), PowerSync fetches the list of available programs from Tesla and creates one switch per program. You can now enroll or unenroll directly from HA, the mobile Controls screen, or via automation — no more needing the Tesla app to manage VPP participation.

**Powerwall settings now first-class HA entities**
Backup reserve, operation mode (TOU vs Self-Consumption), grid export rule, and grid charging — previously only callable via services — are now real HA entities (`number`, `select`, and `switch`) on the PowerSync device. You can use them in any HA dashboard or automation without writing service calls. A binary sensor also surfaces whether you've manually overridden the optimiser's export control.

**Unified Tesla API client with Retry-After handling**
New service handlers, mobile API endpoints, and automation actions all flow through a single API helper on the coordinator that handles retries, exponential backoff, and Retry-After headers consistently. This replaces several copies of inline retry logic and makes future Tesla API additions much cleaner.

**New mobile API endpoints**
Three new HTTP endpoints — `/api/power_sync/tesla/storm_watch`, `/api/power_sync/tesla/off_grid_ev_reserve`, and `/api/power_sync/tesla/vpp_programs` — back the new mobile Controls screen widgets. The existing `/api/power_sync/powerwall_settings` response is also extended with a capabilities block, current Storm Watch state, current off-grid EV reserve, and the site's country code so the app knows which controls to render.

---

### 2.11.1 — Release-notes workflow fix

**Discord notifications now include the full release notes**
The release workflow was generating notes from git commit subjects only and then filtering out the version-bump commit, leaving an empty notes file. The Discord notification then read that empty body. The workflow now prefers `RELEASE_NOTES.md` (committed alongside the version bump) and only falls back to commit-log generation when the file is missing. The duplicate inline Discord notification block has been removed so each release now sends exactly one Discord message containing the proper release notes.

Update available via HACS
