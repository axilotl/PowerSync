<!-- release: v2.12.494 -->

## What's Changed

**Price-Level Charging is now a manual EV mode**
Price-Level Charging now shares the same battery-protection behavior as Scheduled Charging. The integration accepts the new Preserve Home Battery option for price-based manual charging, keeps it mutually exclusive with No Grid Import, and publishes the correct optimizer intent while price-level charging is active.

**Scheduled Charging supports No Grid Import**
Scheduled Charging now passes the No Grid Import setting into the dynamic EV charge path, so both manual EV charging modes expose the same home-battery choices and enforce them consistently.

Update available via HACS
