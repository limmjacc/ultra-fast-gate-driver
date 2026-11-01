# Target IC: CY8C4125LQI-S425 (Infineon PSoC 4100S)

## Confirmed 2026-11-01, from the physical part marking

The project owner photographed the chip on the target board. The marking
reads:

```
CY8C4125
LQI-S425
2219 A 03
CYP616078
PHI    DC
300
```

**Full part number: CY8C4125LQI-S425** — QFN package ("LQ"), Industrial
temperature range ("I"), S-Series ("S"). Decoding Infineon's own part
numbering convention (read directly from the PSoC 4100S datasheet, Table 42):

| Digit(s) | Value | Meaning |
|---|---|---|
| Architecture | 4 | PSoC 4 |
| Family | 1 | 4100 family |
| **CPU speed** | **2** | **24 MHz** |
| Flash capacity | 5 | 32 KB |
| Package | LQ | QFN |
| Temperature | I | Industrial |
| Series | S | S-Series |

This resolves the ambiguity raised in the earlier version of this document:
**this specific chip is the PSoC 4100S family, QFN package, 24 MHz maximum
CPU/IMO speed** — not 48 MHz. Infineon's own PSoC 4100S datasheet (saved as
`hardware/datasheets/infineon-cy8c4125-psoc-4100s-datasheet.pdf`, document
002-00122 Rev. *K) lists every CY8C4125 ordering variant in its family,
including several close to this one (CY8C4125LQI-S412/S413/S422/S423/
S432/S433), **all at 24 MHz**; the exact attribute suffix "-S425" was not
itself listed in that table's visible rows, but the nomenclature decode above
is unambiguous and consistent across every CY8C4125 variant shown in both the
PSoC 4100S and PSoC 4100PS datasheets, so 24 MHz can be treated as confirmed
for this chip regardless of the exact attribute code.

**The project's earlier working assumption that the target IC runs at
48 MHz (from the period before the crowbar topology was adopted — see
[../decisions/decision-log.md](../decisions/decision-log.md), entries 8 and
9) does not hold for this actual chip.** It is a real correction, not a
refinement: 24 MHz means a 41.7 ns clock period (double the 20.8 ns period
48 MHz would have given), which loosens, not tightens, the timing-resolution
argument made in [05-host-interface.md](05-host-interface.md) about the
BeagleBone PRU's granularity relative to the target's own clock.

## What this changes from the previous (ambiguous) version of this document

The electrical analysis below is **unchanged in substance** — it was read
from the sibling PSoC 4100PS datasheet, and cross-checking it directly
against this confirmed chip's own PSoC 4100S datasheet shows the power
system, decoupling recommendations, absolute maximum ratings, and POR/BOD
thresholds are the same figures in both documents (see
[../reference/datasheet-notes.md](../reference/datasheet-notes.md) for the
side-by-side). What changes is confidence: these figures are now read from
the correct family's own datasheet, not a plausible sibling's, and the clock
speed is corrected from 48 MHz to the confirmed 24 MHz.

## What this is: a flash-based Arm Cortex-M0+ MCU, not a simple analog IC

This remains true and unaffected by the family correction. It is a small
microcontroller with on-chip flash, SRAM, an internal 1.8 V core regulator,
and analog peripherals — not a fixed-function part.

- **It has its own internal voltage regulator between the pin being
  crowbarred and its own digital core**, which may filter short glitches
  before they reach the logic that actually executes code — see "How the
  glitch reaches the core" below.
- **It has flash memory**, a known sensitive point in published
  fault-injection literature on this class of device: supply dips during
  flash operations are a standard mechanism by which voltage glitching
  causes exploitable faults on flash-based MCUs generally, not only on this
  specific part. The PSoC 4100S datasheet itself notes flash writes can take
  up to 20 ms and warns against resetting the device (including via
  "improper power supply levels") during that window — directly relevant to
  planning when in the target's operation a glitch is likely to matter most.

## Power system (confirmed against the PSoC 4100S datasheet)

Three supply-related pins: **VDDD** (digital supply, the pin this fixture
crowbars), **VDDA** (analog supply), **VCCD** (the internal 1.8 V regulator's
output, which powers the digital core).

> "The VCCD pin must be bypassed to ground via an external capacitor
> (0.1 µF; X5R ceramic or better) and must not be connected to anything
> else." — PSoC 4100S datasheet, Power section

The PSoC 4100S datasheet's own power diagram ties VDDA directly to the analog
domain (no separate analog regulator — "the analog circuits run directly
from the VDD input"), and its example bypass schematic shows VDDD and VDDA as
separate pins each with 1 µF + 0.1 µF, both referenced to the same external
supply. **The project owner has confirmed that VDDD and VDDA are physically
interrupted together on this board** — both pins are included in the
crowbar's target node, consistent with the design assumption already in
[01-topology.md](01-topology.md) and
[04-timing-and-recovery.md](04-timing-and-recovery.md).

This design's 3V3 operating point places the device in **Mode 1**
(1.8–5.5 V external supply, internal regulator active, VCCD = 1.8 V derived
internally). Mode 2 (1.71–1.89 V external supply, regulator bypassed, VDDD
tied to VCCD) does not apply here. The PSoC 4100S datasheet adds one detail
not seen in the 4100PS sibling text: **the internal regulator can be disabled
in firmware** — not used by this design, but worth knowing if the test plan
ever wants to run the chip with VDDD driving the core directly.

**Datasheet-recommended decoupling (Mode 1): 1 µF in parallel with 0.1 µF on
VDDD and on VDDA; 0.1 µF on VCCD.** This is what the project owner's decision
to remove decoupling eliminates for this test (see
[../decisions/decision-log.md](../decisions/decision-log.md), entry 10) —
confirmed to be the same recommendation in this chip's actual family
datasheet, not just the sibling used earlier.

## How the glitch reaches the core: the internal regulator may filter it

Unchanged from the previous version of this analysis, and the project owner
has agreed a depth/duration sweep (rather than a single fixed glitch target)
is the right test-design approach going forward:

The digital core runs from VCCD, not directly from VDDD, and VCCD has its own
separate 0.1 µF bypass capacitor. A very short VDDD glitch may be partially
or fully filtered by the regulator and VCCD's capacitor before it reaches the
core logic — **Estimate**, a direct consequence of the architecture, not a
figure the datasheet states outright. This means:

- A glitch that looks dramatic at VDDD is not guaranteed to cause a
  core-logic fault.
- **The test plan is a glitch depth/duration sweep**, to find the range that
  actually propagates through to the core — the project owner has confirmed
  this will be designed as part of the test code, separately from this
  board's hardware design.
- Whether VCCD's own capacitor (a different pin, not reachable by this
  crowbar as currently designed) should also be addressed remains open — see
  [../open-items.md](../open-items.md).

## Logic levels, reset behavior, and absolute ratings

Confirmed consistent between the PSoC 4100S and PSoC 4100PS datasheets:

- **VDDD/VDDA absolute maximum:** −0.5 V to 6 V relative to VSS. A crowbar
  release that rings below −0.5 V (realistic if gate-loop or board
  inductance is not controlled, per
  [04-timing-and-recovery.md](04-timing-and-recovery.md)'s caveats) risks
  exceeding this and damaging the part outside the intended test.
- **Power-on Reset (POR):** rising trip voltage 0.80–1.5 V, falling trip
  voltage 0.70–1.4 V.
- **Brown-out Detect (BOD) for VCCD:** trip voltage 1.48–1.62 V in active and
  sleep modes, 1.11–1.5 V in Deep Sleep.
- **CPU/IMO clock: confirmed 24 MHz maximum** for this exact part (corrected
  from the project's earlier 48 MHz working assumption, as explained above).

## Consequences for this design

- **Confirmed node composition:** VDDD and VDDA together, per the project
  owner, as this document already assumed.
- **A glitch depth/duration sweep is the test plan**, agreed with the project
  owner — this document's job is to support that sweep electrically (fast,
  tunable collapse/recovery via the parallel Rs and delay footprints in
  [04-timing-and-recovery.md](04-timing-and-recovery.md) and
  [02-pulse-generation.md](02-pulse-generation.md)), not to fix a single
  target width.
- **The corrected 24 MHz clock** loosens, rather than tightens, any future
  timing-alignment work relative to the target's own clock period (41.7 ns
  vs. the previously assumed 20.8 ns).
- **VDDD/VDDA's −0.5 V to 6 V absolute maximum** remains the concrete numeric
  limit for the ringing concern in
  [06-safety-and-protection.md](06-safety-and-protection.md).

## Open items specific to this IC

- Decide whether VCCD's decoupling (separate from VDDD/VDDA) also needs to be
  removed or otherwise accounted for, given the filtering effect described
  above.
- Design the glitch depth/duration sweep test code (the project owner has
  taken this on separately).
- Confirm board-level ringing on crowbar release stays within −0.5 V to 6 V
  at VDDD/VDDA.
