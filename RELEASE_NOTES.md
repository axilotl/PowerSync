<!-- release: v2.12.515 -->

## What's Changed

**Custom external-controller planning mode**
PowerSync now includes a `Custom / external controller` battery system for users who already manage their battery hardware through Home Assistant, Node-RED, MQTT, or another control layer. During setup, users select their existing battery level, battery power, grid power, solar power, and home load entities; PowerSync uses those values to build Smart Optimization plans in monitoring mode without sending battery or inverter control commands.

**FoxESS H3-Smart PV3 telemetry**
FoxESS H3-Smart and H3-Pro direct Modbus telemetry now reads the third PV string power register and includes it in the total solar power calculation. This improves optimizer input and dashboard telemetry for systems where PV3 production was previously omitted.

Update available via HACS
