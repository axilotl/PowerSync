<!-- release: v2.12.654 -->

## What's Changed

**EV loadpoints no longer show a phantom `_default` row**
The mobile EV loadpoint status now hides the legacy internal `_default` charging session when it cannot be matched to a single real vehicle and multiple real Tesla loadpoints are already active. This prevents the EV screen and dashboard from showing an extra `_DEFAULT` charger row alongside the actual vehicles during multi-EV scheduled charging.

Update available via HACS
