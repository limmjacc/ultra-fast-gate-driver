# Open items

Everything still undecided, unverified, or unmeasured, grouped by subsystem.
Items resolved earlier and later superseded are in
[decisions/decision-log.md](decisions/decision-log.md), not repeated here.

## Blocking: target IC

1. ~~Get the target Infineon IC's part number.~~ **Answered 2026-11-01:**
   CY8C4125, an Infineon PSoC 4 Arm Cortex-M0+ microcontroller.
2. ~~Get the full ordering code (family/speed-grade/package).~~ **Answered
   2026-11-01**, from a photograph of the physical chip marking:
   **CY8C4125LQI-S425** — PSoC 4100S family, QFN package, Industrial
   temperature range, **24 MHz** maximum CPU/IMO clock (corrected from an
   earlier 48 MHz working assumption). See
   [design/08-target-ic.md](design/08-target-ic.md).
3. ~~Confirm the figures in design/08-target-ic.md against the correct
   family's own datasheet.~~ **Answered 2026-11-01:** read directly from the
   PSoC 4100S datasheet (saved as
   `hardware/datasheets/infineon-cy8c4125-psoc-4100s-datasheet.pdf`) and
   confirmed identical to the PSoC 4100PS figures already documented
   (decoupling values, absolute maximums, POR/BOD thresholds).
4. ~~Confirm whether VDDD and VDDA are tied together on the actual board.~~
   **Answered 2026-11-01:** yes, confirmed by the project owner — both pins
   are physically interrupted together.
5. Decide whether VCCD's own decoupling capacitor (the internal regulator's
   output, separate from the crowbarred VDDD/VDDA pins) also needs
   addressing, given that it may filter short VDDD glitches before they
   reach the digital core — see
   [design/08-target-ic.md](design/08-target-ic.md). **Still open.**
6. Measure or estimate the IC's real input/pin capacitance at VDDD and VDDA
   (shorted together), to replace the FET-COSS-based estimate currently
   used. **Still open.**
7. ~~Define the required glitch width/depth range and resolution.~~
   **Decided 2026-11-01:** a glitch depth/duration sweep, not a single fixed
   width, is the right approach — the project owner is designing the sweep
   test code separately from this board's hardware. The board's job is to
   keep both knobs (via Rs and the delay element) adjustable; see
   [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md) and
   [design/02-pulse-generation.md](design/02-pulse-generation.md).
8. Confirm whether the IC needs more than one supply pin crowbarred, or just
   one (assumed: one channel; VDDD and VDDA are a single node regardless,
   since they are shorted on the board). **Still open.**

## Driver and FET

9. Re-confirm digikey.ca stock for LMG1025QDEERQ1 and BSS806NH6327XTSA1 in a
   browser before ordering (see [reference/sourcing.md](reference/sourcing.md)
   and [reference/data-reliability.md](reference/data-reliability.md)).
10. Measure the BeagleBone's 5 V rail under the driver's actual load against
    the LMG1025-Q1's 4.75–5.25 V recommended range.
11. Confirm the BeagleBone GPIO used actually delivers at least 2.6 V (the
    driver's VIH maximum) under real load, not just the datasheet's 4 mA test
    condition.
12. Confirm BSS806N's gate ringing stays within its ±8 V absolute maximum once
    real gate-loop inductance is in the circuit (see
    [design/06-safety-and-protection.md](design/06-safety-and-protection.md)).

## Pulse generation and timing

13. Confirm the AM3358's L3_CLK frequency (assumed 200 MHz) against the
    processor documentation.
14. Pick the BeagleBone trigger pin: a genuine PRU direct-output pin, not one
    of the sixteen boot-strap pins.
15. Decide the delay-element implementation: RC-plus-buffer footprint set
    (default) versus a programmable delay line (Data Delay Devices 3D3428 or
    equivalent — availability unverified).
16. Choose the actual RC/delay footprint value set once the glitch
    depth/duration sweep design (item 7, above) specifies a range.

## Safety and protection

17. Design and verify the hardware maximum on-time circuit (independent of
    the BeagleBone/PRU) before first power-up.
18. Choose the bench supply's current limit deliberately against the
    stuck-on power table in
    [design/06-safety-and-protection.md](design/06-safety-and-protection.md),
    not just "higher is fine."
19. Size the Rs footprints' power rating, or add a fuse, for continuous
    stuck-on operation at each populated value.
20. Confirm board-level ringing on crowbar release stays within the target
    IC's −0.5 V to 6 V VDDD/VDDA absolute maximum (see
    [design/08-target-ic.md](design/08-target-ic.md)).

## Board and process

21. Build a SPICE model of the crowbar node (FET, Rs, driver output
    impedance, estimated parasitics) in `simulation/` and compare against
    [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md)'s
    hand estimates before ordering.
22. ~~Create the KiCad project and library tables in `hardware/`.~~
    **Done 2026-11-01:** `hardware/ultra-fast-gate-driver.kicad_pro`,
    `sym-lib-table`, `fp-lib-table`, and a first-pass schematic
    (`hardware/ultra-fast-gate-driver.kicad_sch`) now exist, with U1, Q1, the
    gate resistors, bypass caps, the Rs bank, the IN- placeholder, the LED,
    and generic connector placeholders placed and wired. **Still needed:** a
    real footprint/header for the target IC connection once its full
    ordering code and package are confirmed (CY8C4125LQI-S425 is QFN, but
    this board connects to it via a cable/header, not by hosting the chip
    itself — J3 is currently a generic 2-pin placeholder).
23. **Resolve one remaining ERC item on the schematic:** `kicad-cli sch erc`
    reports a `multiple_net_names` warning (and a related `pin_to_pin` error
    on the two PWR_FLAG markers) saying the TRIG label and the +5V net near
    J1 are "attached to the same items." Direct inspection of the file's wire
    coordinates found no actual overlapping segment, and removing the
    PWR_FLAGs entirely does not clear it, so the cause is narrower than a
    simple wiring mistake — likely a net-naming interaction specific to how
    local (non-global) labels merge with an unnamed power-symbol net. This
    is best resolved interactively in the KiCad GUI: open the schematic, run
    Inspect → Electrical Rules Checker, and use "Highlight Net" on the TRIG
    label and on the +5V symbol near J1 to see exactly what KiCad considers
    connected. Every other wiring in the schematic was verified correct by
    direct visual inspection (see
    [decisions/decision-log.md](decisions/decision-log.md) for the pin-
    coordinate convention this uncovered and fixed).
24. Lay out the parallel Rs and delay-element footprints described in
    [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md) and
    [design/02-pulse-generation.md](design/02-pulse-generation.md) — the
    schematic places the Rs bank (4 resistors, 3 marked DNP) but the delay
    element is still just a placeholder (R5).
25. Four-layer (or higher) stackup, per the LMG1025-Q1's layout requirements —
    pick a fab and confirm capability.
26. Confirm the Würth LED's forward voltage against its own datasheet (only
    distributor listings were available at selection time).
27. Decide on a scope-friendly probe pad at the target node with a short
    ground return, for measuring actual glitch shape.
28. Pick real connector part numbers for J1 (BeagleBone interface), J2 (3V3
    supply in), and J3 (target node out) — all three are currently generic
    `Connector_Generic` placeholders in the schematic, not vendored parts.

## Review

29. Review the complete design — including the maximum on-time protection,
    Rs sizing/fusing, and the scope note in
    [design/06-safety-and-protection.md](design/06-safety-and-protection.md) —
    with a qualified engineer before first power-up against a real target IC.
