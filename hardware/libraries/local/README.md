# Local libraries

Symbols, footprints, and 3D models authored specifically for this board —
anything not adequately covered by a vendored third-party library.

- `symbols/local.kicad_sym` — power symbols copied unmodified from KiCad's
  own bundled `power.kicad_sym` (CC-BY-SA 4.0 — see
  [`../vendored/ti-lmg1025-q1/license-cc-by-sa-4.0.md`](../vendored/ti-lmg1025-q1/license-cc-by-sa-4.0.md)):
  `+5V`, `+3V3`, `GND`, `PWR_FLAG`. Copied in for full self-containment
  rather than relying on KiCad's global library table, matching this
  project's library policy (see [`../../README.md`](../../README.md)).
- `footprints.pretty/` — project-original footprints (none yet).
- `3dmodels/` — project-original 3D models (none yet).
