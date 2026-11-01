# Hardware

KiCad 10 project for the gate driver board. Follow the same policy as
custom-wireless-mouse: every symbol, footprint, and 3D model is vendored
inside this folder and referenced through `${KIPRJMOD}`-relative paths.

## Opening the project

Open `ultra-fast-gate-driver.kicad_pro` in KiCad 10. The project's
`sym-lib-table` and `fp-lib-table` are picked up automatically, giving you
the vendored driver and FET symbols/footprints ready to use.

## Layout

```
hardware/
├── ultra-fast-gate-driver.kicad_pro  Project file
├── ultra-fast-gate-driver.kicad_sch  Schematic — first pass, see status below
├── sym-lib-table                     Project-local symbol library table
├── fp-lib-table                      Project-local footprint library table
├── datasheets/       PDF datasheets for every non-passive part, kebab-case named
├── libraries/
│   ├── local/        Power symbols copied from KiCad's bundled library
│   └── vendored/     One directory per part, each with its own ATTRIBUTION.md
├── fab-outputs/      Gerbers, drill, pick-and-place, BOM per revision
└── 3d-renders/       Exported board renders
```

## Schematic status

A first-pass schematic exists with U1 (LMG1025-Q1), Q1 (BSS806N), the gate
resistors, VDD bypass caps, the Rs bank (4 footprints, 3 marked DNP), the
IN- placeholder (R5), the power LED, and generic connector placeholders for
J1–J3 placed and wired. See
[../docs/decisions/decision-log.md](../docs/decisions/decision-log.md) entry
13 for how it was built and verified, and
[../docs/open-items.md](../docs/open-items.md) items 22–28 for what's still
open on it — notably one unresolved ERC warning near J1 best checked
interactively in the GUI, and the delay element and connectors, which remain
placeholders.

No PCB layout exists yet (`.kicad_pcb` not created). When you get there,
include the parallel, solder-selectable footprints for the series resistor
and pulse-delay element described in
[../docs/design/04-timing-and-recovery.md](../docs/design/04-timing-and-recovery.md)
and
[../docs/design/02-pulse-generation.md](../docs/design/02-pulse-generation.md),
and the four-layer-minimum stackup the LMG1025-Q1's datasheet calls for.
