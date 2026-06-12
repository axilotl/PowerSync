<!-- release: v2.12.627 -->

## What's Changed

**Other / Custom TOU setup opens the custom tariff form directly**
Selecting Other / Custom TOU during first-time setup now opens the custom tariff setup instead of routing through the GloBird / AEMO settings screen. This makes manual fixed-rate and time-of-use setup clearer for non-Australian and non-GloBird users, while still allowing rates to be skipped and configured later.

**Custom TOU setup title and regression coverage**
New Custom TOU entries now use a matching setup title, and focused config-flow tests cover the direct custom tariff route so the setup path does not regress back through unrelated provider settings.

Update available via HACS
