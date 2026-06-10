<!-- release: v2.12.617 -->

## What's Changed

**Optimizer actions apply at tariff boundaries**
Smart Optimization now applies the current cached schedule action during the normal coordinator refresh when the schedule crosses into a new action. This lets free-import charge windows start on the actual tariff boundary, such as 11:00 for GloBird ZeroHero, instead of waiting for the next full LP solve before force charge is sent to the battery.

**Startup polling resumes after the first optimization**
The startup optimization task now clears its task handle once it finishes, and the interval polling loop only waits while that startup task is still running. This prevents a completed startup solve from suppressing later wall-clock optimizer cycles.

Update available via HACS
