<!-- release: v2.12.385 -->

## What's Changed

**Keep NeoVolt surplus balancer settings live after saving options**
PowerSync now persists NeoVolt connection changes into the options payload Home Assistant uses to reload the integration. This prevents the independent stack surplus balancer from staying on an older runtime value, such as `disabled`, after the UI has been saved back to Auto.

**Restore anti-fighting behavior for multi-stack NeoVolt installs**
Multi-inverter NeoVolt systems that rely on PowerSync's balancer can now have the Auto setting take effect immediately after the options flow is saved, so PowerSync can park a stack when one battery starts charging while another is discharging under Normal mode.

Update available via HACS
