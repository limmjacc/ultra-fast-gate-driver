# Requirements

See [decisions/decision-log.md](decisions/decision-log.md) for how these were
arrived at, including requirements that were stated and then superseded.

## Purpose

Pull a target IC's 3V3 supply input down to ground for a controlled,
nanosecond-scale duration, then release it back to 3V3, to test the IC's
tolerance to brief supply transients. See
[design/06-safety-and-protection.md](design/06-safety-and-protection.md) for
what this does and does not test (it is not a lightning-surge test).

## Fixed

- **Trigger input:** from a BeagleBone Black, 3V3 logic, active high.
- **Target rail:** 3V3 maximum anywhere in the system; no hazardous voltages.
- **Grounding:** the BeagleBone, this board, and the target IC's board share
  one logic ground. No isolation required — see
  [reference/isolation-analysis.md](reference/isolation-analysis.md).
- **Target decoupling:** removed for this test, by the project owner's
  decision, to keep the target node's RC time constant small. See
  [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md).
- **Glitch width goal:** sub-20 ns is the ideal, as low as achievable. See
  [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md) for
  the achievable range under the current design.
- **Glitch pulse generation:** the LMG1025-Q1 driver's delayed-AND method
  (IN+ / IN-), with parallel, solder-selectable footprints for the delay
  element and for the series resistor (Rs), so both can be tuned on the
  bench. See [design/02-pulse-generation.md](design/02-pulse-generation.md)
  and [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md).
- **Board supply:** 5 V, from the BeagleBone's own rail.
- **Power-present indicator:** an SMD LED; any part is acceptable.
- **Target load current (superseded context):** an earlier resistive-load
  model assumed 7 mA at 3.3 V; this no longer applies under the crowbar
  topology but is kept in the decision log for history.
- **Supply current capacity:** not a hard constraint — a higher-current,
  current-limited bench supply can be used if needed. See
  [design/06-safety-and-protection.md](design/06-safety-and-protection.md)
  for why the current limit still needs to be chosen deliberately.

## Target IC: CY8C4125LQI-S425 (Infineon PSoC 4100S)

**Confirmed 2026-11-01** from the physical chip's top marking: Infineon PSoC
4100S family, QFN package, Industrial temperature range, **24 MHz** maximum
CPU/IMO clock (not 48 MHz — correcting an earlier working assumption from
before the crowbar topology was adopted). It is an Arm Cortex-M0+
microcontroller with on-chip flash, not a fixed-function IC. VDDD and VDDA
are confirmed physically interrupted together on this board. See
[design/08-target-ic.md](design/08-target-ic.md) for the full analysis,
including why the chip's own internal regulator (between the crowbarred pin
and the digital core) may filter very short glitches.

## Open (blocking final part/footprint values)

| Parameter | Status |
|---|---|
| Target IC's real input/supply capacitance (VDDD + VDDA, shorted together) | Unknown; estimated from the FET's own COSS in the meantime (see [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md)) |
| Whether VCCD's separate internal-regulator decoupling also needs addressing | Open — VCCD is not on the crowbarred pin, but may filter the glitch before it reaches the digital core; see [design/08-target-ic.md](design/08-target-ic.md) |
| Glitch depth/duration sweep design | Agreed as the right test approach; the project owner is designing this separately from the board hardware |
| Rs footprint value set | Planned as parallel footprints (4.7 Ω / 10 Ω / 22 Ω / 33 Ω candidates); final values pending the sweep design above |
| Bench supply current limit | Not yet chosen; see [design/06-safety-and-protection.md](design/06-safety-and-protection.md) |
| Form factor and connectors | Not yet specified |
| Number of channels | Assumed one |

See [open-items.md](open-items.md) for the full working checklist.
