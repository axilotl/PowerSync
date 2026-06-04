<!-- release: v2.12.570 -->

## What's Changed

**Provider login errors now show correctly**
GloBird and Flow Power portal login failures in the options flow now use provider-specific error messages instead of falling back to Home Assistant's generic unknown-error text. This covers invalid credentials, GloBird captcha prompts, Flow Power SMS verification failures, and provider portal connection failures.

**Better diagnostics for provider portal changes**
Unexpected GloBird and Flow Power portal login failures are now logged with the underlying exception, and failed Flow Power login clients are cleaned up before retrying. This makes future provider-side login changes easier to diagnose from the Home Assistant logs.

Update available via HACS
