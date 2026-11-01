# Hardware

KiCad project for the gate driver board. Follow the same policy as
custom-wireless-mouse: every symbol, footprint, and 3D model is vendored
inside this folder and referenced through `${KIPRJMOD}`-relative paths.

```
hardware/
├── datasheets/       PDF datasheets for every non-passive part, kebab-case named
├── libraries/
│   ├── local/        Symbols/footprints authored for this project
│   └── vendored/     One directory per part, each with its own ATTRIBUTION.md
├── fab-outputs/      Gerbers, drill, pick-and-place, BOM per revision
└── 3d-renders/       Exported board renders
```

The KiCad project files (`ultra-fast-gate-driver.kicad_pro`, `.kicad_sch`,
`.kicad_pcb`) have not been created yet. Create them from KiCad 10 inside this
folder once the target IC's part number is known — see
[../docs/open-items.md](../docs/open-items.md). The driver (TI LMG1025-Q1)
and FET (Infineon BSS806N) are already selected; see
[../docs/design/03-driver-and-fet.md](../docs/design/03-driver-and-fet.md).
When laying out the schematic, include parallel, solder-selectable footprints
for the series resistor and pulse-delay element described in
[../docs/design/04-timing-and-recovery.md](../docs/design/04-timing-and-recovery.md)
and
[../docs/design/02-pulse-generation.md](../docs/design/02-pulse-generation.md).
