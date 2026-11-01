# Documentation

This project is a bench fixture: it takes a trigger from a BeagleBone Black
and uses it to crowbar (short to ground, then release) a 3V3 supply rail on a
target Infineon control IC, for nanoseconds at a time, to test the IC's
tolerance to supply transients. It is not a general-purpose gate driver board
and not a lightning-surge test fixture; see
[design/06-safety-and-protection.md](design/06-safety-and-protection.md) for
the scope note.

**Status (2026-11-01):** concept and electrical analysis only. No schematic,
PCB, or simulation exists yet. This is an exploratory, hobbyist-scale project
— every document here is a working set of notes and estimates, not a
validated or finished design. See
[how to read this project](decisions/decision-log.md#how-to-read-this-project)
for more on that.

## Where to start

- **New to this project?** Read [decisions/decision-log.md](decisions/decision-log.md)
  first. It is the structured record of how the design arrived at its current
  shape, in order, including the ideas that were tried and dropped.
- **Building or reviewing the circuit?** Start at [design/README.md](design/README.md).
- **Checking a figure or a part number?** Start at [reference/README.md](reference/README.md).
- **What's left to do?** See [open-items.md](open-items.md).
- **What is this board required to do?** See [requirements.md](requirements.md).

## Layout

```
docs/
├── README.md                 This file
├── requirements.md           Current requirements, fixed and open
├── open-items.md             Checklist of everything still undecided or unverified
├── decisions/
│   └── decision-log.md       Structured, chronological record of every design decision
├── design/                   How the circuit works and why, organized by subsystem
│   ├── 01-topology.md
│   ├── 02-pulse-generation.md
│   ├── 03-driver-and-fet.md
│   ├── 04-timing-and-recovery.md
│   ├── 05-host-interface.md
│   ├── 06-safety-and-protection.md
│   ├── 07-power-and-indicator.md
│   └── 08-target-ic.md
└── reference/                 Source material: datasheet figures, stock checks, analyses
    ├── datasheet-notes.md
    ├── sourcing.md
    ├── isolation-analysis.md
    └── data-reliability.md
```
