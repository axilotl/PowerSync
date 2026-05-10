<!-- release: v2.12.363 -->

## What's Changed

**Capacity-aware Neovolt stack balancing**
Neovolt multi-inverter systems can now enter usable battery capacity for each selected stack, such as `20.1, 30.2`, directly in the setup and Configure flows. PowerSync uses those values to weight fleet SOC and split charge or discharge requests by stack size, so mismatched batteries move at the same SOC rate instead of blindly receiving equal power.

**Safer setup for uneven battery stacks**
The Neovolt balancer now prefers configured stack capacities over sensor-reported capacity when provided, exposes stack capacity in balancer diagnostics, and validates that users enter one positive capacity per selected Neovolt integration.

Update available via HACS
