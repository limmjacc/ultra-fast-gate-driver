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
19. **Done 2026-11-23:** real connector part numbers picked and verified in
    stock on digikey.ca (J1 Sullins PRPC004SAAN-RC, J2 and JT Sullins
    PRPC002SAAN-RC). See [reference/bom.md](reference/bom.md).

24. **Done 2026-11-23:** full BOM picked and verified. Every part, including all
    passives and connectors, is confirmed in stock on a live digikey.ca page and
    recorded on the schematic (MPN, DigiKey PN, DigiKey link, datasheet,
    package). See [reference/bom.md](reference/bom.md). Still re-confirm stock at
    order time, and confirm the Wurth LED forward voltage (item 17) and the Rs
    pulse ratings against the datasheets before first use.

## Schematic

20. **Done 2026-11-22:** the schematic was rebuilt for the general-purpose
    design (trigger buffer, delayed-AND, monostable plus AND max-on-time, Rs
    bank, fuse, clamp, target pads, test points, optional self-supply),
    organised into labeled functional blocks, and passes ERC with zero
    violations. Remaining schematic work is cosmetic label placement, done in
    the KiCad GUI.

## Library and output hygiene

22. Vendor the remaining standard parts into the project-local libraries. The
    custom/critical parts (LMG1025-Q1, BSS806N) are already copied into
    `hardware/libraries/`, but the commodity symbols (Device:R/C/D/LED/Fuse,
    74xGxx logic, Connector_Generic, Connector:TestPoint, power symbols) and
    their footprints still point at KiCad's global libraries. At layout time,
    make the project self-contained and upgrade-safe with File -> Export ->
    Symbols to New Library and Export Footprints to New Library, relink, then
    Tools -> Update Schematic from PCB. This is a GUI step (footprint relink
    needs the PCB), so it waits for layout.
23. Extend the job set (`hardware/ultra-fast-gate-driver.kicad_jobset`) with the
    PCB outputs (Gerbers, Excellon drill, position/pick-and-place, STEP) once
    the PCB exists, so a single Run regenerates the whole fab package.

## Review

21. Review the complete design, including the max-on-time circuit, Rs
    sizing/fusing, and the scope note in
    [design/06-safety-and-protection.md](design/06-safety-and-protection.md),
    with a qualified engineer before first power-up against a real board.
