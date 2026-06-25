<!-- release: v2.12.718 -->

## Fixes

- Prevent Profit Max and export actions from draining below the Auto-Apply export bridge reserve.
- Compute the export-only floor from the final post-processed schedule, including spread export and No Idle conversions.
- Keep Auto-Apply reserve lowering intact while enforcing the separate hardware reserve plus forecast home-load bridge for export commands.
