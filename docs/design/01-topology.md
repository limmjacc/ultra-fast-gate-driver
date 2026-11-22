# Topology

## What this board does

It pulls a target board's supply rail down to ground for a controlled,
nanosecond-scale duration, then releases it. This is a supply-rail crowbar
used for glitch fault injection. It is general-purpose: it works on any small
microcontroller board with a rail up to 5.5 V. See
[06-safety-and-protection.md](06-safety-and-protection.md) for what this test
does and does not cover.

## Block diagram

```
BeagleBone Black        this board                                   target board
───────────────         ───────────────────────────────────────     ────────────
PRU GPIO (3V3) ─trig─▶ buffer ─┬─────────────── IN+ ┐
                               │                     │ LMG1025-Q1    OUTH ─Rg─┐
                               └─ RC delay ──── IN- ─┘ gate driver   OUTL ─Rg─┤ gate
                                                       (5 V)                  │
      one-shot max on-time ── gates IN+ (AND) ────────┘                    BSS806N
                                                                             │ FET
                                                                   drain ────┤
                                                                     │       │
            Rs (series) ── fuse ── TARGET pad ─clip/solder─▶ target rail     │
                                       │                                      │
       shared logic ground ───────────┴──────────────────────────── source ─┘
```

The FET drain connects through the series resistor Rs and a fuse to the target
pad, which clips or solders with short leads onto the target's live rail. The
FET source returns to the shared ground. Driving the gate high shorts the rail
to ground through Rs; releasing it lets the rail recover, restored by the
target's own supply. See [03-driver-and-fet.md](03-driver-and-fet.md) for the
driver and FET, [02-pulse-generation.md](02-pulse-generation.md) for how the
pulse width is set, and [04-timing-and-recovery.md](04-timing-and-recovery.md)
for how Rs and the small node capacitance set the glitch shape.

## Crowbar the live rail, with an optional self-supply

The default mode is to crowbar the target's own live rail. The target board
powers and restores its own rail; the fixture only shorts it briefly through
Rs. This suits clipping onto arbitrary boards. Rs limits the current drawn from
the target supply during the glitch and sets how hard the rail is pulled down.

An optional self-supply footprint (J2 and a DNP series jumper Rsup) lets a
bench supply source the target rail through the fixture instead, for cases
where the target is not powered on its own. It is not populated by default.

## Keeping the node small

The glitch is sharpest when the capacitance on the injected node is small. In
practice the node is a few millimetres of copper at the target's supply pin,
plus the FET's own output capacitance and the probe. The local decoupling
capacitor at that pin is desoldered for the test, which removes the largest
source of node capacitance and lets the rail collapse and recover quickly. See
[04-timing-and-recovery.md](04-timing-and-recovery.md).

## Grounding: one shared logic ground, no isolation

The BeagleBone Black, this board, and the target board all share one logic
ground. The maximum voltage anywhere is 5.5 V, and no hazardous voltage
exists. Under those conditions no galvanic isolation is used: there is no
voltage difference to isolate across, and the fastest digital isolators would
be far too slow for this design. The full reasoning, including what would
change this conclusion, is in
[../reference/isolation-analysis.md](../reference/isolation-analysis.md).

Practical consequence: tie the trigger signal ground to the FET source return
at a single point near the FET, per the driver datasheet's ground-bounce
guidance (see [03-driver-and-fet.md](03-driver-and-fet.md)), and keep the lead
from the target pad to the target rail short.

## What is deliberately not in this design

- **No isolation** (see above).
- **No decoupling at the injection node during the test.** Removed to keep the
  node RC small; see [04-timing-and-recovery.md](04-timing-and-recovery.md).
- **No through-hole power path.** Lead inductance (roughly 5 to 10 nH per leg)
  is incompatible with nanosecond edges, so the driver, FET, and gate loop are
  SMD. Only connectors and the target pads are through-hole or clip points.
- **No active high-side restore switch, for now.** The target restores its own
  rail in live-rail mode. An active restore across Rs is deferred unless
  measurements show the passive recovery is too slow.
