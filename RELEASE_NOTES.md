<!-- release: v2.12.520 -->

## What's Changed

**Tesla optimizer export survives reload handoff**
PowerSync now prevents an older restore-normal task from clearing a newer optimizer force-discharge command while Tesla API calls are still in flight. This fixes a race where the dashboard could correctly show an export plan, but Powerwall would be switched back to self-consumption shortly after a Home Assistant reload or PowerSync update.

Update available via HACS
