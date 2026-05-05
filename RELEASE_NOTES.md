<!-- release: v2.12.295 -->

## What's Changed

**Tesla export windows now match the optimizer plan**
Tesla Powerwall LP export and discharge actions now upload a force-discharge tariff that covers the full contiguous optimizer export window instead of only the next 10 minutes. This keeps Tesla's TOU algorithm aligned with longer export periods and prevents the temporary tariff from dropping back to 0c mid-window.

**GloBird tariff restore protection**
PowerSync now refuses to save or restore any temporary force-mode tariff as the normal Tesla TOU tariff. Tariffs containing Force Charge, Force Discharge, PowerSync force utility metadata, or force-mode tariff codes are ignored as restore candidates, and the last known valid Tesla tariff is cached as a fallback for static TOU users such as GloBird.

Update available via HACS
