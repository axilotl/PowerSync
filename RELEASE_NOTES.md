<!-- release: v2.12.353 -->

## What's Changed

**NeoVolt multi-inverter battery balancing**
PowerSync now detects the battery-to-battery fighting pattern where the lower-SOC NeoVolt stack is discharging while the higher-SOC stack is still charging. When this happens, PowerSync parks the higher-SOC stack in No Battery Charge so the lower stack can catch up instead of having one battery feed the other.

**NeoVolt app automation state**
PowerSync app automations now read state from NeoVolt battery coordinators, along with the other supported inverter coordinators. This lets NeoVolt automations evaluate battery, grid, and price conditions correctly from the app.

Update available via HACS
