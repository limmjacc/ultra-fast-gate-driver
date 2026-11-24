# Fabrication outputs

Generated manufacturing exports from the KiCad project - Gerbers, drill
files (Excellon), pick-and-place / position files, and BOM exports.

Nothing in this folder is hand-edited, and nothing in it is committed (it is
git-ignored). Regenerate everything in one step from the job set.

## One-click regeneration (job set)

`../ultra-fast-gate-driver.kicad_jobset` holds the output recipe. Run it from
the KiCad **Jobs** panel (open the project, Tools -> Jobs, pick the fab-outputs
destination, Run), which is the supported path for every job including the BOM.

The schematic PDF job also runs headless:

```
kicad-cli jobset run --file hardware/ultra-fast-gate-driver.kicad_jobset \
    hardware/ultra-fast-gate-driver.kicad_sch
```

Note: the BOM job needs the KiCad GUI kiface and writes an empty file under the
headless CLI, so run the full set from the Jobs panel. Standalone
`kicad-cli sch export bom` works headless if you only want the BOM.

The job set currently covers the schematic outputs (PDF, BOM). Add the PCB jobs
(Gerbers, Excellon drill, position/pick-and-place, STEP) to the same job set
once `ultra-fast-gate-driver.kicad_pcb` exists; see
[../../docs/open-items.md](../../docs/open-items.md).

Suggested convention once the board has real revisions:

```
fab-outputs/
└── rev-a/
    ├── gerbers/
    ├── ultra-fast-gate-driver-rev-a.zip   (fab-house-ready archive)
    ├── BOM.csv
    └── positions.csv
```
