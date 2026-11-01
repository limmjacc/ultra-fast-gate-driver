---
name: ti-lmg1025-q1-attribution
---

# TI LMG1025-Q1 gate driver — attribution

- **Symbol** (`ti-lmg1025-q1.kicad_sym`): hand-drawn, original artwork (a plain
  rectangle body), with pin names and numbers taken directly from the
  datasheet's pin table (Table 4-1, DEE package): pin 1 = IN+, pin 2 = GND,
  pin 3 = VDD, pin 4 = OUTH, pin 5 = OUTL, pin 6 = IN-, pin 7 = the exposed
  thermal pad (numbered 7 on TI's own DEE0006A mechanical drawing), tied to
  GND per the datasheet's layout guidance.
  - Source: `hardware/datasheets/ti-lmg1025-q1-datasheet.pdf` (TI document
    SNOSD74C, revised December 2024), section 4 (Pin Configuration and
    Functions).
- **Footprint** (`wson-6-2x2mm-dee0006a.pretty/wson-6-2x2mm-dee0006a.kicad_mod`):
  copied from KiCad's own official library
  (`Package_DFN_QFN.pretty/DFN-6-1EP_2x2mm_P0.5mm_EP0.7x1.6mm.kicad_mod`),
  then renamed. Chosen as the closest standard match to TI's own DEE0006A
  land pattern: 2 mm × 2 mm body, 6 pins at 0.5 mm pitch, exposed pad length
  1.6 mm matches TI's drawing exactly.
  - Upstream source: <https://gitlab.com/kicad/libraries/kicad-footprints>
  - License: CC-BY-SA 4.0 — full text at
    [`license-cc-by-sa-4.0.md`](license-cc-by-sa-4.0.md).
  - **Known discrepancy, not yet resolved:** TI's own DEE0006A land pattern
    specifies the exposed pad at 0.9 mm × 1.6 mm; the closest available
    KiCad bundled footprint has a 0.7 mm × 1.6 mm pad (narrower by 0.2 mm).
    The individual signal pin pads (0.5 mm pitch, land dimensions) match
    TI's drawing. **Verify this against TI's land pattern drawing (datasheet
    section 12, "Example Board Layout") before fabrication** — this narrower
    pad is a safe (undersized, non-solder-mask-defined) direction to err in,
    but it has not been widened to match TI's exact recommendation.
- **3D model:** none available. No bundled KiCad 3D model exists for the
  exact footprint variant used above (the nearby `EP0.61x1.42mm` variant has
  one, but its land pattern doesn't match as closely). The footprint's
  `(model ...)` directive was removed rather than point at a mismatched or
  nonexistent file. Open item: find or create a WSON-6 2x2mm 3D model if a
  rendered board view is needed.

## Part selection

Datasheet: `hardware/datasheets/ti-lmg1025-q1-datasheet.pdf` (TI document
SNOSD74C, revised December 2024), downloaded directly from ti.com and read in
full before selection. See
[`../../../docs/design/03-driver-and-fet.md`](../../../docs/design/03-driver-and-fet.md)
for the selection rationale and
[`../../../docs/reference/datasheet-notes.md`](../../../docs/reference/datasheet-notes.md)
for the extracted electrical figures.

Ordering part: **LMG1025QDEERQ1** (WSON, DEE package, large tape and reel).
The sibling **LMG1025QDRVRQ1** uses the DRV package (DRV0006C), which has
different mechanical dimensions — do not substitute its footprint for this
one without re-checking the package code on the physical part.
