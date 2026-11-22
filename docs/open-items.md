# Open items

Everything still undecided, unverified, or unmeasured, grouped by subsystem.
Items resolved earlier and later superseded are in
[decisions/decision-log.md](decisions/decision-log.md), not repeated here.

## Target (per board, not fixed)

1. This fixture is general-purpose; there is no single target. For any board,
   before glitching: identify the supply pins, any internal regulator between
   the crowbarred pin and the core, the local decoupling to remove, the supply
   absolute maximums (for the ring clamp), and the reset/brown-out thresholds.
   [design/08-target-ic.md](design/08-target-ic.md) is a worked example.
2. Measure or estimate the real node capacitance at the injection point once
   decoupling is removed, to replace the FET-COSS-based estimate. **Per board.**
3. The glitch is a depth/duration sweep, not a single fixed width. The board
   keeps both knobs adjustable (Rs and the delay element); the sweep test code
   is written separately.

## Driver, FET, and logic

4. Re-confirm digikey.ca stock in a browser before ordering (prices in
   [reference/sourcing.md](reference/sourcing.md) are from a 2026-11-22 check).
5. Measure the BeagleBone's 5 V rail under the driver's actual load against the
   LMG1025-Q1's 4.75 to 5.25 V recommended range.
6. Confirm BSS806N gate ringing stays within its 8 V absolute maximum once real
   gate-loop inductance is in the circuit.
7. Match the propagation delays of the IN+ path (through the AND gate) and the
   IN- path (through the RC and buffer), so the AND gate delay does not eat into
   the minimum achievable glitch width.

## Pulse generation and timing

8. Confirm the AM3358 L3_CLK frequency (assumed 200 MHz) against the processor
   documentation.
9. Pick the BeagleBone trigger pin: a genuine PRU direct-output pin, not one of
   the sixteen boot-strap pins.
10. Choose the RC delay footprint value set, and decide whether to also lay out
    the programmable delay line (Data Delay Devices 3D3428 or equivalent,
    availability unverified).

## Safety and protection

11. Choose Tmax (Rmt, Cmt) for the max-on-time one-shot: well above the intended
    glitch, short enough to protect Rs from a stuck-on fault.
12. Size the Rs footprints for stuck-on power at 5.5 V, or fuse them. Pick F1's
    rating against the stuck-on currents in
    [design/06-safety-and-protection.md](design/06-safety-and-protection.md).
13. Clamp the target node in both directions. D2 (Schottky to ground) covers the
    undershoot; add a high-side clamp (TVS or Schottky to the rail, or a
    bidirectional TVS) for the release kickback the SPICE model shows. Pick low
    forward voltage and low capacitance so the clamp does not load the node. Add
    the high-side clamp to the schematic.
14. Confirm board-level ringing on crowbar release stays within the target's
    supply absolute maximum (negative and positive).

## Board and process

15. SPICE model of the crowbar node exists in `simulation/`; compare its results
    against [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md)
    and update both if they disagree. Re-run with real board parasitics before
    ordering.
16. PCB layout not started. Four-layer or better stackup per the LMG1025-Q1
    layout requirements; pick a fab and confirm capability.
17. Confirm the Wurth LED forward voltage against its own datasheet (only
    distributor listings were available at selection time).
18. Scope-friendly probe pad at the target node with a short ground return
    (TP5 is placed; confirm its ground return on layout).
19. Pick real connector part numbers for J1 (BeagleBone tap), J2 (optional
    supply in), and the target pads; they are generic placeholders in the
    schematic.

## Schematic

20. **Done 2026-11-22:** the schematic was rebuilt for the general-purpose
    design (trigger buffer, delayed-AND, monostable plus AND max-on-time, Rs
    bank, fuse, clamp, target pads, test points, optional self-supply),
    organised into labeled functional blocks, and passes ERC with zero
    violations. Remaining schematic work is cosmetic label placement, done in
    the KiCad GUI.

## Review

21. Review the complete design, including the max-on-time circuit, Rs
    sizing/fusing, and the scope note in
    [design/06-safety-and-protection.md](design/06-safety-and-protection.md),
    with a qualified engineer before first power-up against a real board.
