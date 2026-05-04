## What's Changed

**Solax PV string telemetry now exposes the detail panel properly**
Solax Hybrid installs now publish PV1, PV2, and PV3 string-level power,
voltage, and current sensors through PowerSync. This is especially useful for
X3 Ultra setups where the third string previously disappeared into the total
solar figure, making it hard to spot a weak string, shading issue, or MPPT
imbalance from Home Assistant. The Solax bridge also recognizes more of the
entity names emitted by the upstream Solax Modbus integration, falls back to
the string total when the aggregate solar sensor is missing or stale, and keeps
the dashboard scene clean by leaving string telemetry in the details table
instead of cluttering the main power-flow graphic.

**Home Assistant startup is cleaner for Powerwall local control**
PowerSync now preloads the Powerwall local protobuf transport off the Home
Assistant event loop before registering the local pairing and off-grid control
endpoints. That avoids the startup warning about `google._upb._message` being
imported inside the event loop while keeping the actual Powerwall local runtime
lazy and unchanged.

**Non-Tesla installs no longer wait on Tesla-only number setup**
The capability-gated Tesla number task now only starts when a Tesla energy site
is configured. FoxESS, GoodWe, Sigenergy, Sungrow, AlphaESS, and other
non-Tesla installs no longer register a background poller that can hold Home
Assistant startup open while it waits for Tesla capabilities that will never
arrive. A regression test now checks that the task is actually enclosed by the
Tesla guard instead of merely appearing after one in the file.

**FoxESS H3-Smart battery voltage uses the live pack voltage again**
H3-Smart battery voltage scaling was corrected from 0.01 V to 0.1 V. Systems
that were reporting roughly 48 V for a high-voltage pack should now report the
real 480-560 V range, which lets force-charge and force-discharge calculations
use the live voltage instead of falling back to the conservative 500 V default.

Update available via HACS
