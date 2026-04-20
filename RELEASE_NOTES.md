## What's Changed

**Flow Power: Tariff Code Dropdown Now Populates After Selecting a DNSP**
When selecting a network distributor (DNSP) for the first time, the tariff code dropdown was showing only a blank "—" option because the tariff codes are loaded at form render time — before the user has made a selection. Both the initial setup flow and the options flow now detect this case: if a network is selected but no tariff codes were available to choose from, the form re-renders with that network's codes loaded, keeping the DNSP selection intact. Users can now complete a two-step selection: pick your DNSP, then pick your tariff code on the same screen.

Update available via HACS
