## What's Changed

**HA dashboard home image overlay text restored**
The latest home scene refresh moved the generated text layout coordinates into absolute SVG space, but the card was still applying them inside translated node groups. That caused the wording overlay on the home image to disappear even though the animated power flow lines still rendered. The generated scene positions are now normalized before they are applied, so the labels and power text appear correctly again across the dashboard scenes.

Update available via HACS
