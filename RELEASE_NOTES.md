<!-- release: v2.12.482 -->

## What's Changed

**Restore Discord release notes**
PowerSync's release automation now tracks the last release that was successfully posted to Discord and can backfill any missed release notes in order. This prevents temporary GitHub Actions failures or manual release fallbacks from permanently dropping HACS release announcements.

**Harden release cleanup**
Release notes are now cleared only after Discord notification succeeds, and the Discord marker is advanced only after every pending release in the batch has posted. This keeps future releases from skipping older missed announcements while still preventing duplicate Discord posts.

Update available via HACS
