# Topology

## What this board does

It pulls a target IC's 3V3 supply input down to ground for a controlled,
nanosecond-scale duration, then releases it back to 3V3 — a supply-rail
"crowbar" — to test the target IC's tolerance to brief supply transients.
See [06-safety-and-protection.md](06-safety-and-protection.md) for what this
test does and does not cover.

## Block diagram

```
BeagleBone Black                 this board                      target IC board
─────────────────               ─────────────────────────────    ────────────────
PRU GPIO (3V3) ──trigger───▶ IN+ ┐
                                  │  LMG1025-Q1          OUTH ──▶ gate ┐
delay element ───delayed───▶ IN- ┘  gate driver                        │  BSS806N
                                     (5 V supply)         OUTL ──▶     ┘  FET
                                                                        │
     3V3 supply ──[ Rs, parallel ]──────────────────────── node ───────┤── target IC
     (bench, current-limited)                              (probe pad)  VDD pin
                                                                        │
     GND ───────────────────────────────────────────────── shared ─────┘ GND
     (one shared logic ground across all three boards)
```

The FET's drain sits on the target node (the IC's VDD pin, fed through Rs
from the 3V3 supply); its source returns to the shared ground. Driving the
gate high shorts the node to ground; releasing it lets the node recover
through Rs. See [03-driver-and-fet.md](03-driver-and-fet.md) for the driver
and FET themselves, and [04-timing-and-recovery.md](04-timing-and-recovery.md)
for why Rs — not the FET — sets the recovery time once decoupling is removed.

## Grounding: one shared logic ground, no isolation

The BeagleBone Black, this board, and the target IC's board all share one
logic ground. The maximum voltage anywhere in the system is 3V3, and no
hazardous voltage exists. Under those conditions, no galvanic isolation is
used on the trigger input or anywhere else on this board — there is no
voltage difference to isolate across, and the fastest available digital
isolators would themselves have been too slow for the speed this design
needs. The full reasoning, including what would change this conclusion, is in
[../reference/isolation-analysis.md](../reference/isolation-analysis.md).

Practical consequence: tie the signal ground for the trigger input to the
FET's source return at a single point near the FET, per the driver
datasheet's ground-bounce guidance (see
[03-driver-and-fet.md](03-driver-and-fet.md)).

## What is deliberately not in this design

- **No isolation** (see above).
- **No decoupling capacitor on the target IC's supply pin for this test.**
  This was a deliberate choice to keep the node's RC time constant small; see
  [04-timing-and-recovery.md](04-timing-and-recovery.md). It assumes the IC
  can tolerate running without its normal decoupling for the duration of the
  test — confirm this once the part number is known
  ([../open-items.md](../open-items.md)).
- **No through-hole power path.** Lead inductance (roughly 5–10 nH per leg)
  is incompatible with nanosecond edges, so the driver, FET, and gate loop
  are all SMD. Only connectors are through-hole.
- **No active high-side restore switch**, for now. An active switch across Rs
  could restore the rail faster than a passive resistor after release, at the
  cost of a second gate drive channel and break-before-make timing. Deferred
  unless the passive Rs approach (entry in
  [04-timing-and-recovery.md](04-timing-and-recovery.md)) proves insufficient
  once real measurements are available.
