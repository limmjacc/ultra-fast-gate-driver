# Decision log

A chronological, structured record of how this project's design arrived at
its current shape. Each entry is what was decided, why, and what it
superseded. This is a design history, not a schematic — see
[../design/README.md](../design/README.md) for the current circuit, and
[../open-items.md](../open-items.md) for what is still unresolved.

## How to read this project

This is an exploratory, hobbyist-scale electronics project, not a validated
or production design. Everything in this `docs/` tree is a working set of
notes and estimates, several explicitly marked as such, not a finished
or reviewed design. The board itself is a bench test fixture: it
intentionally injects electrical faults into another board to see how that
board responds, so it carries real risk of damaging the target chip or the
fixture itself if built and used carelessly — treat the safety notes
throughout this project as practical lab precautions, not a formal safety
case.

## 1. Initial brief: an ultra-fast gate driver

**Decided:** build a board, organized like the `custom-wireless-mouse`
project (KiCad hardware, `docs/`, no firmware folder needed here), that takes
a 3V3 or 5V logic trigger and uses it to "slam open" a power MOSFET gate with
a nanosecond-scale turn-off.

**Why:** that was the original request. The repo was scaffolded with
`hardware/`, `simulation/`, and `docs/hardware/` (since reorganized into the
structure this file lives in), plus a draft requirements list with most
parameters marked TBD.

## 2. First part search: driver and FET for a fast edge

**Decided:** TI LMG1025-Q1 (WSON, 5 V, 7 A source / 5 A sink, sub-3 ns
propagation delay) as the gate driver, with Infineon BSS138N and BSS806N as
candidate FETs, based on a web search for fast, low-charge, 3V3-compatible
parts.

**Why:** the driver's datasheet shows propagation delay and edge times far
inside a 5 ns budget, and 3V3-logic compatibility (checked later, see entry
4) was plausible from search summaries. No through-hole part was found that
could meet nanosecond switching — lead inductance rules it out — so the
design went SMD-only from this point on.

**Superseded by:** entry 7 (the gate-drive load model changed once the real
application — a crowbar, not a gate load — was known).

## 3. Load defined: 3V3 drain, 7 mA, through-hole preference

**Decided:** the FET was assumed to switch a 3.3 V, 7 mA load (a small IC
supply), drain at 3.3 V, source at 0 V. Through-hole was preferred if
available; none was found, so SMD was confirmed.

**Why:** this was the project owner's answer when asked for the missing
parameters. It shaped every subsequent capacitance/resistance estimate until
entry 8.

## 4. Datasheet audit: 3V3 compatibility confirmed, with a caveat

**Decided:** downloaded and read the TI and Infineon datasheets directly
(saved to `hardware/datasheets/`) rather than relying on search summaries.
Confirmed the LMG1025-Q1 accepts a 3.3 V logic input, with VIH at 2.6 V
maximum — meaning the host GPIO must guarantee at least 2.6 V under load, a
real but narrow margin. Confirmed the BSS138N switches the stated 7 mA load
with ample margin. Estimated the drain edge (using the FET's COSS against the
471 Ω equivalent load) at roughly 13 ns, missing the original 5 ns goal,
because the *load resistance*, not the driver, set the limit.

**Why:** the project owner asked for the claims to be audited against the
actual datasheets rather than taken from search summaries, which had already
disagreed with each other once (stock figures in particular). See
[../reference/data-reliability.md](../reference/data-reliability.md) for why
that distinction matters throughout this project.

**Superseded by:** entry 7 (the whole 471 Ω-load model stopped applying once
the real application was known).

## 5. Stock check: BSS138N not orderable

**Decided:** checked digikey.ca (delivery to Edmonton, Alberta) and found the
Infineon BSS138N and BSS138W both at zero stock with 41–48 week lead times.
Substituted the Diodes BSS138-7-F (same SOT-23 footprint, in stock) for a
first build, while flagging that its datasheet gives only maximum
capacitance figures, which makes the drain-edge estimate weaker.

**Why:** a part that cannot be bought is not a selection. This pattern — pick
a part on datasheet merit, then verify it is actually orderable — repeats at
every part decision in this project; see
[../reference/sourcing.md](../reference/sourcing.md) for the current
consolidated stock table.

**Superseded by:** entry 7 (BSS806N replaced both BSS138 variants once the
crowbar topology was chosen).

## 6. Isolation question: not needed

**Decided:** no galvanic isolation on the trigger input.

**Why:** the project owner confirmed that the BeagleBone Black, this board,
and the IC board under test all share one logic ground, that 3V3 is the
maximum voltage anywhere in the system, and that no hazardous voltage exists.
Under those conditions there is no voltage to isolate across. Separately, the
fastest commercially available digital isolators found (5–17 ns delay) would
have cost more delay than the entire original 5 ns turn-off budget. See
[../reference/isolation-analysis.md](../reference/isolation-analysis.md) for
the full reasoning, including the conditions that would change this
conclusion (a floating or differently-referenced target rail, any hazardous
voltage, or a long inter-chassis cable).

## 7. Reframed: this is a crowbar fault-injection fixture, not a gate-load driver

**Decided:** the actual application is to pull a 3V3 supply input on a target
IC down to ground and release it, for nanoseconds at a time, to test the IC's
transient/glitch tolerance — not to drive a resistive gate load at all. This
changed which FET properties matter (low RDS(on) and low gate charge, not
drain-edge speed into a fixed resistor) and introduced a new element: a
series resistor (Rs) between the 3V3 supply and the target node, through
which the node recovers after the FET releases.

**Why:** the project owner stated the actual test purpose. The FET was
re-selected: Infineon BSS806N (57 mΩ max RDS(on) at 2.5 V gate, 1.7 nC gate
charge) replaced the BSS138 variants, which were far too resistive for a
crowbar. A first-order Rs/node-capacitance model was built to size the
recovery tail. This also explicitly reframed the then-current 48 MHz
switching-rate analysis (entry 8) as describing the IC's own clock rate, not
a FET switching requirement.

**Scope note added:** a nanosecond supply dropout tests glitch and brown-out
tolerance; it is not a lightning-surge immunity test. Formal surge and
fast-transient immunity testing (the kind referenced by standards like
IEC 61000-4-5 and IEC 61000-4-4) is a different, much more involved test setup
and is out of scope for this fixture.

## 8. A detour: 48 MHz switching rate (superseded)

**Decided (then undone):** for a brief period, the design assumed the FET had
to toggle a signal at the target IC's 48 MHz clock rate. Analysis showed this
was not achievable with the 471 Ω load model (needed under ~5 pF of total node
capacitance, which neither candidate FET met) and that the BeagleBone's PRU
cannot produce exactly 48 MHz (it steps in multiples of 5 ns, giving 50 MHz or
40 MHz, not 48 MHz, assuming a 200 MHz PRU clock that was never confirmed
against the processor documentation).

**Why superseded:** entry 7 clarified that 48 MHz is the target IC's own
operating clock, relevant only to how finely the crowbar's timing should be
resolved relative to that clock — not something the FET itself needs to
toggle at. The BeagleBone PRU timing finding is still useful and carried
forward into
[../design/05-host-interface.md](../design/05-host-interface.md).

## 9. Sub-20 ns glitch target, decoupling identified as the real limiter

**Decided:** the project owner set a goal of "ideally sub-20 ns" for the
glitch width, confirmed the target as "a typical control IC from Infineon"
(part number not yet known), and confirmed the 3V3 supply could be fed from a
higher-current, current-limited bench supply if needed.

**Finding:** with a *typical* decoupling capacitor left on the target's
supply pin (estimated 100 nF), the node collapses quickly but then recovers
through Rs on a timescale of hundreds of nanoseconds to microseconds — the
decoupling capacitor, not the FET or the series resistor, would have set the
real glitch width, regardless of how precisely the trigger pulse was timed.

**Also decided:** the LMG1025-Q1's two-input AND-gate structure (drive IN+
with the trigger and a delayed copy of it into IN-; the output pulses high
for exactly the delay between them) is a better way to generate a narrow
pulse than relying on the BeagleBone PRU's 10 ns-minimum, 5 ns-stepped output
directly. This needs a hardware delay element between IN+ and IN-, which is
the part of the design the next entry makes adjustable.

**Superseded by:** entry 10 (the project owner chose to remove the
decoupling capacitor entirely rather than work around it, which changes the
numbers in this entry substantially — for the better).

## 10. Decoupling removed; parallel footprints for flexibility; delayed-AND adopted

**Decided (current design baseline):**

1. **No decoupling capacitor on the target IC's supply pin for this test.**
   The project owner chose to remove it rather than design around its RC
   time constant, for "a clean input to IC."
2. **The delayed-AND pulse generation method (entry 9) is adopted** as the
   primary way to set glitch width, with the BeagleBone PRU setting only the
   glitch's timing offset.
3. **Parallel, solder-selectable footprints** for both the series resistor
   (Rs) and the IN+/IN- delay element, so the glitch width, recovery
   behavior, and crowbar current can all be tuned on the bench without a
   respin, pending the target IC's part number and real input capacitance.
4. The whole repository was reorganized into the structure this file lives
   in, consolidating what had been several overlapping documents
   (`48mhz-analysis.md`, `crowbar-design.md`, and parts of
   `datasheet-audit.md`) into the current `design/` and `reference/` trees.

**Why this is better than entry 9's plan:** without a decoupling capacitor,
the node capacitance the FET has to pull down is just the FET's own output
capacitance plus stray board and pin capacitance — on the order of 200–300 pF,
not the 1–100 nF range a typical decoupling capacitor would add. Recomputing
with that smaller, de-rated capacitance (the FET's COSS is specified at 10 V
in its datasheet and is meaningfully higher at the circuit's actual 3.3 V,
since output capacitance rises as drain voltage falls) gives:

- **Collapse (turn-on):** the RC time constant through the FET's ~57 mΩ
  on-resistance into ~225 pF is on the order of tens of *picoseconds* —
  negligible. The real floor on how fast the node can be pulled down is the
  gate driver's own turn-on propagation delay (2.6 ns typical, 4.1 ns
  maximum), not the RC network.
- **Recovery (release):** this is now the dominant, and the only meaningfully
  tunable, timescale. It is set by Rs times the same ~225 pF, giving roughly
  2–5 ns at Rs = 4.7–10 Ω up to roughly 50 ns at Rs = 100 Ω. See
  [../design/04-timing-and-recovery.md](../design/04-timing-and-recovery.md)
  for the full table and the reasoning behind picking a default Rs.

This means the sub-20 ns goal is achievable with real margin using Rs values
in the 10–33 Ω range, once decoupling is out of the picture — a materially
better result than entry 9's microsecond-scale recovery estimate. The
driver's own propagation delay (a few ns) is now the practical floor on
glitch width, not the RC network.

**What remains open:** the target IC's part number, its real input
capacitance and supply tolerance (both unknown without it — see
[../design/04-timing-and-recovery.md](../design/04-timing-and-recovery.md)
for why the ~225 pF figure is an estimate built on the FET's own
capacitance, not a measurement of the real target), and whether the IC can
tolerate having its decoupling removed at all. These are tracked in
[../open-items.md](../open-items.md).

## 11. Target IC identified as CY8C4125 — an Infineon PSoC 4 MCU, with a part-number ambiguity

**Decided:** the project owner gave the target IC's part number: CY8C4125.

**Finding:** this is not a simple fixed-function "control IC" as assumed
earlier — it is an Infineon PSoC 4 series microcontroller (Arm Cortex-M0+,
on-chip flash, SRAM, and an internal 1.8 V core regulator). Reading
Infineon's own PSoC 4100PS datasheet (002-22097 Rev. *F, the closest direct
match for this base part number) directly rather than relying on search
summaries, two things stood out:

1. **"CY8C4125" alone does not specify one device.** The same base number is
   used across at least three different PSoC 4 sub-families (4100, 4100S,
   4100PS) with different maximum clock speeds for the same digits — notably,
   Infineon's own 4100PS ordering table shows CY8C4125 variants as the
   **24 MHz** speed grade *in that family*, while a distributor lists a
   CY8C4125 variant in the *4100S* family at 48 MHz. The earlier
   48 MHz figure given for the target IC (back when it was only "a typical
   control IC from Infineon," entry 9) cannot be confirmed from the bare part
   number "CY8C4125" — the full ordering code is needed. See
   [../design/08-target-ic.md](../design/08-target-ic.md) for the full
   nomenclature breakdown and what to check on the physical part.
2. **The pin this fixture crowbars (VDDD) is not what directly powers the
   digital core.** The chip has its own internal 1.8 V regulator between
   VDDD and the core logic (VCCD), with its own separate bypass capacitor.
   This means a very short VDDD glitch may be partially or fully filtered
   before it reaches the logic the test is trying to disturb — a mechanism
   this project's analysis had not previously needed to consider, because the
   earlier generic "control IC" assumption treated the crowbarred pin as
   feeding the sensitive logic directly.

**Also found and saved:** the datasheet confirms VDDD and VDDA "must be
shorted together on the PCB," meaning the crowbar's target node includes the
analog supply, not just the digital one; absolute maximum ratings (VDDD
−0.5 V to 6 V) that bound how much release ringing this fixture can tolerate
without risking damage outside the intended test; and POR/BOD trip voltages
that describe what the chip itself is expected to do partway through a
glitch.

**Not yet resolved at the time:** the exact full ordering code (which
determines the real maximum clock, package, and confirms the
family-specific figures above), and whether VCCD's separate decoupling
should also be addressed. The first was resolved immediately afterward — see
entry 12. The second remains tracked in [../open-items.md](../open-items.md).

## 12. Full part number confirmed from the physical chip: CY8C4125LQI-S425, 24 MHz, PSoC 4100S

**Decided:** the project owner photographed the chip's top marking, resolving
the ambiguity raised in entry 11. The full part number is
**CY8C4125LQI-S425**: PSoC 4100S family, QFN package, Industrial temperature
range, S-Series.

**Finding:** decoding Infineon's own part-numbering convention (read from the
PSoC 4100S datasheet, saved as
`hardware/datasheets/infineon-cy8c4125-psoc-4100s-datasheet.pdf`) shows the
CPU-speed digit in "CY8C4125" is "2," meaning **24 MHz, not 48 MHz**. This is
a genuine correction to the project's working assumption from before the
crowbar topology was adopted (entries 8–9 assumed the target ran at 48 MHz).
Cross-checking the PSoC 4100S datasheet against the PSoC 4100PS datasheet
used in entry 11 shows the power system, decoupling recommendations,
absolute maximum ratings, and POR/BOD thresholds are identical figures in
both documents — so that electrical analysis stands confirmed, now against
the chip's actual family rather than a plausible sibling.

**Also decided:** the project owner confirmed VDDD and VDDA are physically
interrupted together on the board (matching this design's existing
assumption), and agreed that a glitch depth/duration sweep — not a single
fixed glitch width — is the right test approach, to be designed separately
from this board's hardware.

**Full detail:** [../design/08-target-ic.md](../design/08-target-ic.md),
rewritten with the confirmed part number in place of the earlier ambiguity
analysis.

## 13. KiCad project and first-pass schematic built

**Decided:** populate the actual KiCad project — library tables, vendored
parts, and a first-pass schematic — rather than leave the design as
documentation only. `hardware/ultra-fast-gate-driver.kicad_pro`,
`sym-lib-table`, `fp-lib-table`, and `ultra-fast-gate-driver.kicad_sch` now
exist, with U1 (LMG1025-Q1), Q1 (BSS806N), the gate resistors, VDD bypass
caps, the Rs bank (4 footprints, 3 marked DNP), the IN- placeholder, the
power LED, and generic connector placeholders for J1–J3 all placed and
wired.

**A real, reusable finding came out of building this:** KiCad's symbol
library format stores pin coordinates in a Y-up convention (matching how the
symbol *library editor* displays them), but the schematic *sheet* is Y-down.
Placing a symbol on a sheet negates the pin's local Y before applying the
instance's own rotation — confirmed by testing the real, unmodified
`Transistor_FET:Q_NMOS_GSD` symbol from KiCad's own bundled library, which
showed the identical transform. This matters for this project specifically
because [ti-lmg1025-q1](../../hardware/libraries/vendored/ti-lmg1025-q1/) and
[infineon-bss806n](../../hardware/libraries/vendored/infineon-bss806n/) are
hand-placed (not drawn through the KiCad GUI, which would apply this
transform automatically and invisibly) — any future hand-authored placement
math for these parts, or new vendored parts added the same way, needs to
apply this same Y-negation.

**Verification approach, given the file was built programmatically rather
than drawn in the GUI:** `kicad-cli sch export svg`, rendered and visually
inspected pin-by-pin (not just via `kicad-cli sch erc`'s text output, which
was found to report pin positions inconsistently with the actual rendered —
and electrically real — geometry in at least one case during this process;
treat its coordinates as a rough locator, not ground truth, and confirm
anything it flags against the rendered image or the live GUI). This caught
and fixed several real issues beyond the coordinate convention itself:
overlapping reference/value text on rotated parts, a double-applied vertical
offset, and five backwards sign errors in manually-placed GND/+5V symbol
offsets.

**What's left open on the schematic itself:** one ERC warning
(`multiple_net_names`, TRIG/+5V near J1) that direct file inspection could
not explain and that removing the related PWR_FLAGs did not clear — flagged
in [../open-items.md](../open-items.md) item 23 for a quick interactive check
in the GUI rather than further blind editing. The delay element (R5) and all
three connectors (J1–J3) remain placeholders pending the decisions tracked
elsewhere in the open items list.
