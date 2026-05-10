<!-- release: v2.12.359 -->

## What's Changed

**NeoVolt stack parking now holds both charge and discharge**
PowerSync now parks the higher-SOC NeoVolt stack with Idle (No Dispatch) when balancing force-charge across a multi-stack system. This prevents the parked stack from continuing to discharge house load while the lower-SOC stack is trying to charge, so force-charge periods produce the expected net battery charge.

**Optimizer current action power now shows scheduled intent**
The Current Action sensor now reports the scheduled optimizer power for the active action and exposes sampled live battery power separately as `actual_battery_power_w`. This prevents stale or ramping live power from making an active charge slot look like a tiny command while the hardware is drawing real grid power.

**Observed Tesla sessions now record live EV prices**
Observed Tesla charging sessions now use the same shared EV price lookup as automation actions, including dynamic providers and tariff schedules, so session accounting is costed from the current import/export prices instead of generic defaults.

Update available via HACS
