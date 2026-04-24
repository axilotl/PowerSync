## What's Changed

**Away Mode Redesign — Enable Before Leaving**
Away mode now works as you'd expect: enable it *before* you go on holiday, disable it when you get home. While you're away the LP uses natural low-load history (empty house), which biases it toward exports rather than reserving battery for no one. When you disable the switch on return, a 7-day recovery window starts — the LP automatically excludes the vacation period from its history and backfills with the 7 days before you left, so it plans correctly for your normal consumption right away. The recovery window self-closes after 7 days as new post-return history fills the slot. Short toggles under 1 hour are ignored. State persists across Home Assistant restarts.

*Update available via HACS*
