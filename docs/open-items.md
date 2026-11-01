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
22. Create the KiCad project and library tables in `hardware/`, including a
    CY8C4125LQI-S425 (QFN) footprint/header for the target connection.
23. Lay out the parallel Rs and delay-element footprints described in
    [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md) and
    [design/02-pulse-generation.md](design/02-pulse-generation.md).
24. Four-layer (or higher) stackup, per the LMG1025-Q1's layout requirements —
    pick a fab and confirm capability.
25. Confirm the Würth LED's forward voltage against its own datasheet (only
    distributor listings were available at selection time).
26. Decide on a scope-friendly probe pad at the target node with a short
    ground return, for measuring actual glitch shape.

## Review

27. Review the complete design — including the maximum on-time protection,
    Rs sizing/fusing, and the scope note in
    [design/06-safety-and-protection.md](design/06-safety-and-protection.md) —
    with a qualified engineer before first power-up against a real target IC.
