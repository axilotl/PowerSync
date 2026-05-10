<!-- release: v2.12.372 -->

## What's Changed

**GoodWe reserve restore no longer sticks at an IDLE hold level**
PowerSync now restores the startup reserve target from the configured hardware reserve, the persisted user reserve, or the optimizer floor instead of trusting the inverter's live reserve immediately after an update or restart. This prevents a temporary IDLE hold, such as a GoodWe DOD value that represents 45% reserve, from becoming the permanent restore target when the user had configured 20%.

Update available via HACS
