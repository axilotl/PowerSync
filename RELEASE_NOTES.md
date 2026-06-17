<!-- release: v2.12.668 -->

## What's Changed

**Leave Sigenergy ESS max discharge unchanged during export**

Sigenergy force discharge now drives export with the Remote EMS active power target and grid export limit only, leaving the ESS max discharge control untouched. This keeps household load from reducing the intended grid export during ZeroHero and other export windows, and avoids changing the ESS Max Export value that users may reserve for separate battery/EV control.

Update available via HACS
