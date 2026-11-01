---
name: infineon-bss806n-attribution
---

# Infineon BSS806N FET — attribution

- **Symbol** (`infineon-bss806n.kicad_sym`): copied from KiCad's own generic
  `Device:Q_NMOS_GSD` symbol (pin order Gate/Source/Drain — numbered pin 1 =
  Gate, pin 2 = Source, pin 3 = Drain), then renamed and re-pointed at this
  part's footprint and datasheet. The GSD pin order matches Infineon's
  standard small-signal SOT-23 pinout convention, used consistently across
  this device family (confirmed against the datasheet's package drawing).
  - Upstream source: <https://gitlab.com/kicad/libraries/kicad-symbols>
  - License: CC-BY-SA 4.0 — full text at
    [`license-cc-by-sa-4.0.md`](license-cc-by-sa-4.0.md).
- **Footprint** (`sot-23-bss806n.pretty/sot-23-bss806n.kicad_mod`): copied
  unmodified (geometry) from KiCad's own official library
  (`Package_TO_SOT_SMD.pretty/SOT-23.kicad_mod`), then renamed. Standard
  3-pin SOT-23, matching the datasheet's package designation (PG-SOT23).
  - Same upstream source and license as the symbol.
- **3D model** (`3dmodels/sot-23-bss806n.step`): copied unmodified from
  KiCad's own official 3D model pack
  (`Package_TO_SOT_SMD.3dshapes/SOT-23.step`), same license as above.

## Part selection

Datasheet: `hardware/datasheets/infineon-bss806n-datasheet.pdf` (Infineon,
Rev. 2.3, 2011-07-11), downloaded directly from infineon.com and read in full
before selection. See
[`../../../docs/design/03-driver-and-fet.md`](../../../docs/design/03-driver-and-fet.md)
for the selection rationale (chosen for the crowbar topology on low
on-resistance and low gate charge) and
[`../../../docs/reference/datasheet-notes.md`](../../../docs/reference/datasheet-notes.md)
for the extracted electrical figures.

Ordering part: **BSS806NH6327XTSA1** (SOT-23, 3000 pcs/reel). Confirm this
exact suffix against [`../../../docs/reference/sourcing.md`](../../../docs/reference/sourcing.md)
before ordering — stock figures there came from a page-fetch tool, not a
direct browser check.
