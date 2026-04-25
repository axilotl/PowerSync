## What's Changed

**Sigenergy: force charge no longer suppresses solar**
When the LP optimizer or a manual force charge command was active, Sigenergy was set to "Command Charging — Grid First" mode (mode 3), which tells the inverter to stop solar generation and charge entirely from the grid. This was wrong: the correct mode is "Command Charging — PV First" (mode 4), which charges from solar and draws grid only to make up the difference. The result was that solar output would drop to zero during any charge window, wasting available generation.

**EV Smart Charging: solar surplus detection fixed for Sigenergy, Sungrow, and other non-Tesla batteries**
The EV auto-schedule planner was reporting 0 kW solar and 0 kW load for all non-Tesla battery systems, causing solar surplus charging to never trigger regardless of actual solar output. The root cause was a unit mismatch: Tesla's API returns power in watts, but all other coordinators (Sigenergy, Sungrow, FoxESS, GoodWe, AlphaESS, Solax) store power in kilowatts. The planner was dividing all values by 1000 expecting watts — producing near-zero readings (e.g. 3.97 kW ÷ 1000 = 0.004 kW ≈ 0 kW). The live status builder now converts kW to watts before passing values to the planner. FoxESS, GoodWe, AlphaESS, and Solax users also gain correct live data in the EV planner for the first time (they were previously missing from the live status lookup entirely).

Update available via HACS
