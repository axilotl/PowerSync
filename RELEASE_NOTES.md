## What's Changed

**SAJ H2: Remove Arbitrary SOC Floor on Force Discharge**
The 10% SOC guard added in 2.12.204 was removed. The SAJ inverter enforces its own configurable depth-of-discharge limit via the stanus74 integration, so a hardcoded software floor in PowerSync was redundant and would have blocked legitimate low-SOC discharge commands.

Update available via HACS
