# Documentation

This project is a bench fixture for supply-rail glitch fault injection. It
takes a trigger from a BeagleBone Black and uses it to crowbar (short to
ground, then release) a supply rail on a target board, for a few nanoseconds
at a time, to study how an old or scrap microcontroller responds to brief
supply glitches. It is a general-purpose hobby and learning tool: it works on
any small microcontroller board with a supply rail up to 5.5 V. It is not a
general-purpose gate driver board and not a surge-immunity test fixture; see
[design/06-safety-and-protection.md](design/06-safety-and-protection.md) for
the scope note.

**Status (2026-11-22):** the schematic is complete and passes ERC with no
violations. No PCB layout exists yet, and the board has not been built or
tested. A SPICE model of the crowbar node is in `simulation/`. Every document
here is a working set of notes and estimates, not a validated or finished
design. See
[how to read this project](decisions/decision-log.md#how-to-read-this-project)
for more on that.

## Where to start

- **New to this project?** Read [decisions/decision-log.md](decisions/decision-log.md)
  first. It is the record of how the design arrived at its current shape, in
  order, including ideas that were tried and dropped.
- **Building or reviewing the circuit?** Start at [design/README.md](design/README.md).
- **Checking a figure or a part number?** Start at [reference/README.md](reference/README.md).
- **What is left to do?** See [open-items.md](open-items.md).
- **What is this board required to do?** See [requirements.md](requirements.md).

## Layout

```
docs/
├── README.md                 This file
├── requirements.md           Current requirements, fixed and open
├── open-items.md             Checklist of everything still undecided or unverified
├── decisions/
│   └── decision-log.md       Chronological record of every design decision
├── design/                   How the circuit works and why, by subsystem
│   ├── 01-topology.md
│   ├── 02-pulse-generation.md
│   ├── 03-driver-and-fet.md
│   ├── 04-timing-and-recovery.md
│   ├── 05-host-interface.md
│   ├── 06-safety-and-protection.md
│   ├── 07-power-and-indicator.md
│   └── 08-target-ic.md       A worked example target, not the only target
└── reference/                 Source material: datasheet figures, stock checks, analyses
    ├── datasheet-notes.md
    ├── sourcing.md
    ├── isolation-analysis.md
    └── data-reliability.md
```
