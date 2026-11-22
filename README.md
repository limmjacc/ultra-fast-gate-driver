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

Early design stage. A first-pass schematic exists (vendored driver and
MOSFET parts, 114 of 116 ERC issues resolved, one benign item left
documented); no PCB layout or SPICE simulation exists yet (see
[docs/open-items.md](docs/open-items.md)). The target IC is identified as the
CY8C4125LQI-S425 (PSoC 4100S, Cortex-M0+, 24 MHz max). This design is a
starting point and requires review and validation by a qualified engineer
before use,
including before testing against any real target IC.
