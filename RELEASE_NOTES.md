<!-- release: v2.12.360 -->

## What's Changed

**Energy flow now chooses one grid path**
The built-in PowerSync energy-flow card now picks the dominant grid import/export path for the current scenario instead of lighting multiple grid paths from the same net grid reading. This makes NeoVolt multi-stack behavior easier to read when one stack is charging, another is discharging, or the site is near zero net grid power.

**Price forecast axis labels are no longer clipped**
The dashboard chart renderer now reserves more left-axis space for price units such as `c/kWh`, so electricity price charts show the full label instead of clipping values down to tails like `0.0c/kWh`.

Update available via HACS
