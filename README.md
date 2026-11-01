# ultra-fast-gate-driver

A nanosecond-scale supply-rail crowbar test fixture (KiCad). Triggered by a
BeagleBone Black over a shared 3V3 logic ground, it pulls a target IC's 3V3
supply input to ground and releases it, for a controlled, very short
duration, to test the IC's tolerance to brief supply transients.

This started as a general-purpose ultra-fast gate driver board and was
reframed into its current, more specific purpose partway through design —
see [docs/decisions/decision-log.md](docs/decisions/decision-log.md) for the
full history. **Start at [docs/README.md](docs/README.md)** for requirements,
design, and open items.

## Layout

```
.
├── hardware/     KiCad project — schematic, PCB layout, libraries, datasheets
├── simulation/   SPICE models and results (switching time, gate loop, ringing)
└── docs/         Design documentation — see docs/README.md
```

## Status

Concept and electrical analysis stage. No schematic, PCB layout, or
simulation exists yet, and the target IC's part number is not yet known (see
[docs/open-items.md](docs/open-items.md)). This design is a starting point
and requires review and validation by a qualified engineer before use,
including before testing against any real target IC.
