<!-- release: v2.12.676 -->

## What's Changed

**Show the true battery SOC on the optimizer plan instead of pinning it to the export floor**
When the battery was genuinely below the export floor (the overnight home-load bridge reserve), the 24-hour plan's SOC line clamped up to the floor — so a battery actually at 23% was plotted at the 45% floor, the charge window read the floor instead of the real starting level, and the reported minimum forecast SOC was inflated to the floor. The optimizer's actual dispatch was already correct (it charges and discharges from the real SOC); only the plotted/reported SOC was affected. The plan now reports the true simulated SOC and lets it decline naturally below the export floor as the battery powers the home — the export floor still gates exporting to the grid, it just no longer hides the battery's real level.

Update available via HACS
