# Fabrication outputs

Generated manufacturing exports from the KiCad project — Gerbers, drill
files (Excellon), pick-and-place / position files, and BOM exports.

Nothing in this folder is hand-edited. Regenerate from
`ultra-fast-gate-driver.kicad_pcb` / `.kicad_sch` via **File → Fabrication
Outputs** in KiCad, or with `kicad-cli pcb export gerbers` /
`kicad-cli pcb export drill` / `kicad-cli sch export bom`.

Suggested convention once the board has real revisions:

```
fab-outputs/
└── rev-a/
    ├── gerbers/
    ├── ultra-fast-gate-driver-rev-a.zip   (fab-house-ready archive)
    ├── BOM.csv
    └── positions.csv
```
