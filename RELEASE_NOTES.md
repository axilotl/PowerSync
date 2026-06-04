<!-- release: v2.12.572 -->

## What's Changed

**Fix GloBird portal credential updates from Configure**
PowerSync no longer shows Home Assistant's generic "Unknown error occurred" message when saving GloBird portal email/password details from the dedicated Provider portal login page. The Configure flow now uses the same GloBird credential validation path as initial setup, so valid credentials can be saved and real login failures continue to show the correct GloBird-specific error.

Update available via HACS
