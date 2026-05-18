<!-- release: v2.12.424 -->

## What's Changed

**Stabilized optimizer-owned force charging**
PowerSync now tracks optimizer-issued force charge and discharge windows separately from manual force mode state on non-Tesla systems. This prevents FoxESS and similar hardware-backed systems from cancelling a valid force charge when the LP plan briefly reshuffles the current slot during frequent re-optimization, while still restoring normal mode when the optimizer genuinely stops planning a force action.

**Force commands now use configured power limits when omitted**
Manual force charge and discharge service calls now fall back to the configured optimizer max charge or discharge power when no explicit `power_w` is provided. Explicit service power still wins, so optimizer-generated commands keep their calculated dispatch power.

**Clarified Amber forecast confidence alerts**
The Amber forecast confidence alert now consistently compares predicted prices with the High forecast and labels the setting, notification, and logs around that behavior.

Update available via HACS
