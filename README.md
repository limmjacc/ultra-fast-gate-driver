# ultra-fast-gate-driver

A nanosecond-scale supply-rail crowbar fault-injection fixture (KiCad). A
BeagleBone Black PRU triggers a fast gate driver and a MOSFET that briefly
short a target board's supply rail to ground and release it, for a controlled
few-nanosecond window, to study how an old or scrap microcontroller behaves
when its supply is glitched.

It is a general-purpose bench tool for hobby reverse-engineering and learning,
not tied to one target. It works on any small microcontroller board with a
supply rail up to 5.5 V, clipped or soldered onto with short leads. It is not
a general-purpose gate driver board and not a surge-immunity test fixture; see
[docs/design/06-safety-and-protection.md](docs/design/06-safety-and-protection.md)
for the scope note. **Start at [docs/README.md](docs/README.md)** for
requirements, design, and open items.

## Layout

```
.
├── hardware/     KiCad project: schematic, PCB layout, libraries, datasheets
├── simulation/   SPICE model and results for the crowbar node
└── docs/         Design documentation, see docs/README.md
```

## What it does

The PRU trigger is squared by a logic buffer, split into a direct path and an
RC-delayed path, and fed to the gate driver's two inputs so the output is a
pulse whose width equals the delay (the driver's own delayed-AND method). The
driver switches a low-resistance MOSFET that crowbars the target rail through
a small series resistor Rs. A separate hardware one-shot sets a maximum
on-time so the FET cannot be held on by a stuck trigger or a logic fault. The
target's own decoupling is removed near the injection point to keep the node
capacitance small, so the glitch can be short and sharp.

## Status

Early design stage. The schematic is complete and passes ERC with no
violations. No PCB layout exists yet, and the board has not been built or
tested. The SPICE model of the crowbar node is in `simulation/`. This design
is a starting point and needs review and validation by a qualified engineer
before it is built or used against any real board.
