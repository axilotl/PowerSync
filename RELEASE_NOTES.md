<!-- release: v2.12.567 -->

## What's Changed

**Optimiser decisions now visible in standard logs**
The optimiser's per-cycle decision summary — the planned action mix (`charge`/`export`/`idle`/`self-consumption` steps), solver result, projected daily cost/savings, and the planned battery SOC trajectory — now appears in your Home Assistant logs by default, without needing to switch PowerSync to INFO or DEBUG logging. These two lines are the quickest way to answer "is it planning to charge back up?" or "is it planning to export?" when reviewing behaviour or sending logs for support. This is delivered via a dedicated, narrowly-scoped logger so it does not bring back the verbose debug flood that was removed in a recent release — only these high-value summary lines are surfaced.

**Quieter logs for Powerwall battery pack reconciliation**
The message logged when PowerSync reconciles near-empty expansion battery packs against the aggregate remaining-energy reading has been moved from a warning to debug. This is a routine, expected calculation for some Powerwall configurations, so it no longer clutters your logs as a warning. No behaviour change to the energy figures themselves.

Update available via HACS
