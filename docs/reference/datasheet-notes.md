# Datasheet notes

Figures below were read directly from the PDFs saved in
`hardware/datasheets/`, not from search summaries — see
[data-reliability.md](data-reliability.md) for why that distinction matters.
Items marked **Estimate** are derived in this project, not stated by a
manufacturer.

| File | Revision |
|---|---|
| ti-lmg1025-q1-datasheet.pdf | SNOSD74C, December 2024 |
| ti-lmg1020-datasheet.pdf | SNOSD45B, October 2018 |
| infineon-bss806n-datasheet.pdf | Rev. 2.3, 2011-07-11 |
| infineon-bss138n-datasheet.pdf | Rev. 2.86, 2012-04-17 (superseded selection; see decision log) |
| infineon-bss138w-datasheet.pdf | Rev. 2.43, 2011-07-12 (superseded selection) |
| diodes-bss138-datasheet.pdf | DS30144 Rev. 25-2, June 2024 (superseded selection) |
| ti-am335x-datasheet.pdf | SPRS717L, March 2020 (BeagleBone Black processor) |
| beagleboard-beaglebone-black-manual.pdf | BeagleBoard.org manual, 2026-06-04 |
| infineon-cy8c41x5-psoc-4100ps-datasheet.pdf | Document 002-22097 Rev. *F, 2023-11-16 (sibling family, read before the exact part was confirmed — see note below) |
| infineon-cy8c4125-psoc-4100s-datasheet.pdf | Document 002-00122 Rev. *K, April 2018 (**target IC's actual family, confirmed 2026-11-01**) |

## TI LMG1025-Q1 (selected driver)

- **Package:** 6-pin WSON, 2×2 mm (DRV or DEE pinout variants).
- **Supply:** 4.75–5.25 V recommended, 5.75 V absolute maximum. TI recommends
  holding supply variability within 5% and keeping overshoot within the
  absolute maximum (section 7.2.2.3).
- **UVLO:** rising threshold 4.0–4.35 V, 85 mV hysteresis.
- **Inputs:** VIH 1.7 V typical / 2.6 V maximum; VIL 1.1 V typical / 1.8 V
  maximum; hysteresis 0.38 V minimum. IN+ has a 150 kΩ internal pull-down to
  GND; IN- has a 150 kΩ internal pull-up to VDD. Output = IN+ AND (NOT IN-).
- **Output:** 7 A peak source, 5 A peak sink. Propagation delay 2.6 ns
  (turn-on) / 2.9 ns (turn-off) typical, 4.1 ns / 4.4 ns maximum, into a
  100 pF load. Rise/fall time 650 ps / 850 ps into a 220 pF load. Minimum
  input pulse width that changes the output state: 1.25 ns.
- **Supply current:** 75 µA quiescent; 40 mA (no load) to 51 mA (100 pF load)
  at 30 MHz switching — the datasheet does not characterize higher
  frequencies and recommends burst operation for very high repetition rates
  (section 7.2.2.4).
- **Layout requirements (section 9.1):** a four-layer or higher board;
  0201-package gate resistors/capacitors recommended to minimize inductance;
  place the driver as close to the FET as possible with OUTH/OUTL resistors
  immediately at the gate; source return on layer 2 directly beneath the
  driver and FET; bypass capacitor (0.1–1 µF, X7R or better) on the top layer
  immediately adjacent to VDD, plus an additional 1 µF nearby — TI's own
  example uses a 0.1 µF 0402 plus a 1 µF 0603.
- **Narrow-pulse generation (section 7.2.2.2):** the two-input AND structure
  can generate a pulse of width equal to the delay between IN+ and a delayed
  IN-; see [../design/02-pulse-generation.md](../design/02-pulse-generation.md).

## TI LMG1020 (alternate, not currently selected)

0.8×1.2 mm WCSP, same 5 V / 7 A / 5 A class, faster edges (400 ps typical,
2.5 ns typical / 4.5 ns maximum propagation delay, 1 ns minimum pulse).
Rejected for now on hand-assembly difficulty; see
[../design/03-driver-and-fet.md](../design/03-driver-and-fet.md).

## Infineon BSS806N (selected FET)

- **Package:** SOT-23. BVDSS 20 V. VGS absolute maximum ±8 V.
- **RDS(on):** 41 mΩ typical / 57 mΩ max at VGS = 2.5 V, ID = 2.3 A; 57 mΩ
  typical / 82 mΩ max at VGS = 1.8 V.
- **Gate threshold:** VGS(th) 0.3–0.75 V (typical 0.55 V).
- **Capacitance:** Ciss 370–529 pF; **COSS 118 pF typical / 169 pF maximum at
  VDS = 10 V**, f = 1 MHz; Crss 20–29 pF. See
  [../design/04-timing-and-recovery.md](../design/04-timing-and-recovery.md)
  for why COSS is de-rated upward for this circuit's actual 3.3 V operating
  point.
- **Gate charge:** Qgs 0.55 nC, Qgd 0.58 nC, total Qg 1.7 nC typical at
  VDD = 10 V, ID = 2.3 A, VGS 0 to 2.5 V. Plateau voltage 1.5 V.
- **Switching (at VDD = 10 V, VGS = 2.5 V, ID = 2.3 A, RG = 6 Ω — not this
  circuit's conditions):** turn-on delay 7.5 ns, rise 9.9 ns, turn-off delay
  12.0 ns, fall 3.7 ns. These do not apply directly to the crowbar circuit's
  actual drive and load conditions.
- **Pulsed drain current:** 9.3 A (TA = 25°C).

## Infineon BSS138N / BSS138W, Diodes BSS138-7-F (superseded)

These were selected under the earlier resistive-gate-load model (471 Ω
equivalent load at 7 mA) before the crowbar application was known — see
[../decisions/decision-log.md](../decisions/decision-log.md), entries 2–7.
Kept here for reference since the figures remain accurate, even though the
parts are no longer the current selection:

- **BSS138N:** VGS(th) 0.6–1.4 V typ 1.0 V; RDS(on) 3.3 Ω typical / 4.0 Ω
  maximum at VGS 4.5 V; COSS ≈ 13 pF (read from the typical-capacitance graph
  near VDS = 3 V, not a tabulated figure).
- **BSS138W:** same die family in SOT-323, nearly identical figures to
  BSS138N.
- **Diodes BSS138-7-F:** RDS(on) ≤ 3.5 Ω at VGS 10 V (no 4.5 V figure
  stated); COSS ≤ 25 pF maximum at VDS 10 V (no typical value given — the
  dynamic figures in this datasheet are stated as "guaranteed by design," not
  measured).

## TI AM3358 (BeagleBone Black processor) and the BeagleBone Black manual

See [../design/05-host-interface.md](../design/05-host-interface.md) for the
extracted logic-level, rail, and PRU timing figures — kept there rather than
duplicated here since they are discussed alongside their consequences for
this design.

## Infineon CY8C4125LQI-S425 (target IC) — PSoC 4100S, confirmed

**The full part number was confirmed 2026-11-01** from a photograph of the
physical chip marking: CY8C4125LQI-S425, PSoC 4100S family, QFN package,
Industrial temperature range, 24 MHz maximum CPU/IMO clock (correcting an
earlier 48 MHz working assumption — see
[../decisions/decision-log.md](../decisions/decision-log.md), entries 11–12).
See [../design/08-target-ic.md](../design/08-target-ic.md) for the full
nomenclature decode.

Figures below were originally read from Infineon's PSoC 4100PS datasheet
(002-22097 Rev. *F) before the exact family was known, then cross-checked
directly against this chip's actual family datasheet (PSoC 4100S, document
002-00122 Rev. *K). **Every figure below was confirmed identical between the
two documents** — the only correction needed was the clock speed (24 MHz,
confirmed, not 48 MHz).

- **Architecture:** Arm Cortex-M0+, on-chip flash (32 KB) and SRAM (4 KB),
  internal 1.8 V core regulator. Not a fixed-function analog/power IC.
- **Power pins:** VDDD (digital supply — the pin this fixture crowbars), VDDA
  (analog supply, **must be shorted to VDDD on the PCB** per the datasheet),
  VCCD (internal 1.8 V regulator output that actually feeds the digital
  core, separate from VDDD, with its own bypass capacitor).
- **Supply modes:** Mode 1 (this design's case) — 1.8–5.5 V external supply
  at VDDD/VDDA with the internal regulator deriving VCCD. Mode 2 — 1.71–1.89 V
  external supply with VDDD and VCCD tied together and the regulator bypassed
  (not applicable at this design's 3.3 V).
- **Datasheet-recommended decoupling (Mode 1):** 1 µF in parallel with 0.1 µF
  (X5R ceramic or better) on each of VDDD and VDDA; 0.1 µF (X5R or better) on
  VCCD, stated as not to be connected to anything else. All of this is what
  the project owner's decision to remove decoupling eliminates for this test
  — see [../design/08-target-ic.md](../design/08-target-ic.md) for why VCCD's
  capacitor in particular (not on the crowbarred pin) is worth a separate
  look.
- **Absolute maximum ratings:** VDDD/VDDA −0.5 V to 6 V relative to VSS; VCCD
  −0.5 V to 1.95 V; GPIO −0.5 V to VDD + 0.5 V.
- **Power-on Reset (POR):** rising trip 0.80–1.5 V, falling trip 0.70–1.4 V.
- **Brown-out Detect (BOD) for VCCD:** 1.48–1.62 V (active/sleep), 1.1–1.5 V
  (Deep Sleep).
- **Logic thresholds, CMOS mode:** VIH ≥ 0.7×VDDD, VIL ≤ 0.3×VDDD (at 3.3 V:
  VIH ≥ 2.31 V, VIL ≤ 0.99 V). LVTTL mode (VDDD ≥ 2.7 V): fixed VIH ≥ 2.0 V,
  VIL ≤ 0.8 V.
- **Clock: confirmed 24 MHz maximum** for this exact part (CY8C4125, CPU
  speed digit "2" in Infineon's own nomenclature). The architecture family
  generally supports an IMO adjustable up to 48 MHz in 4 MHz steps
  (±2% tolerance, 7 µs startup time), but the 48 MHz grade in this numbering
  scheme is CY8C4145/CY8C4146, not this chip.
