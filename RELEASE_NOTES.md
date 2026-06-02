<!-- release: v2.12.537 -->

## What's Changed

**Solar surplus EV charging with Sungrow curtailment**
PowerSync now releases Sungrow native export-limit curtailment when Solar Surplus EV charging has an active, plugged-in vehicle that is not full. This lets the inverter raise PV output for the EV instead of staying load-matched after the battery is full and export curtailment has already kicked in.

**Curtailment-aware EV surplus detection**
The EV solar-surplus controller now sees Sungrow native curtailment as a curtailed state, so the existing curtailed/full-battery headroom logic can ramp EV charging from the hidden PV headroom instead of only seeing the small visible grid export.

Update available via HACS
