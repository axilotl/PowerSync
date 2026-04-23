## What's Changed

**HA dashboard text anchoring now matches the scene layout tool**
The dashboard overlays were still offset because the HA card forced text to render with `text-anchor: middle`, while the scene layout tool authored coordinates using the default SVG start anchor. The HA card now uses the same anchor behavior as the layout tool, so labels and values align with the authored scene positions.

Update available via HACS
