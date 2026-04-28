## What's Changed

**SAJ H2: Drop default force charge target from 1000 → 600 to respect battery DC-DC converter rating**
2.12.210 lowered the default sentinel from `1100` → `1000`, but field testing on an H2-10K confirmed the trips were not from AC overload — they were from the battery DC-DC converter overload. The H2-10K has a 10 kW AC inverter but the battery hybrid stage is rated at ~6 kW, and there's no way to tell which rating stanus74's percentage scale maps to without testing each value. To stay safely below the DC stage's rating on the largest H2 model, the default is now `600` (= 60% of rated, ~6 kW). Smaller models will charge slower than their max but won't trip the DC converter. A proper fix later will expose the rated battery DC-DC watts as a config option so each system gets its correct cap.

Update available via HACS
