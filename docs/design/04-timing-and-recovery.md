# Timing and recovery

This is the core sizing analysis for the crowbar: how fast the node collapses
when the FET turns on, how fast it recovers when the FET releases, and what
that means for achieving a sub-20 ns glitch. Everything marked **Estimate**
is derived here, not read from a manufacturer datasheet, and depends on
assumptions that should be revisited once the target IC's part number and a
real board are available (see [../open-items.md](../open-items.md)).

## Why removing the decoupling capacitor matters so much

Before this decision, the node capacitance was assumed to include the
target's decoupling capacitor — typically tens to hundreds of nanofarads on a
real IC supply pin. With a capacitor that large, the node would have
collapsed quickly (it only has to discharge through the FET's low
on-resistance) but then recovered through the series resistor Rs on a
timescale of **hundreds of nanoseconds to microseconds** — the decoupling
capacitor, not the FET, the driver, or Rs, would have set the real glitch
width, however precisely the trigger pulse was timed.

Removing the decoupling capacitor for this test eliminates that bottleneck
entirely. What is left on the node is just the FET's own output capacitance
(COSS) plus whatever stray capacitance the board, the IC's pin, and a
measurement probe add — on the order of 200–300 pF rather than tens of
nanofarads, three orders of magnitude smaller. This is the single biggest
lever in this design for hitting a sub-20 ns glitch.

**This assumes the target IC can run without its normal decoupling for the
duration of the test.** That is a real electrical stress on the IC's own
internal regulation and bypassing, separate from the glitch itself. Confirm
it is acceptable once the part number is known.

## Node capacitance: de-rating COSS to the actual operating voltage

A FET's output capacitance is specified at a particular drain voltage and
falls as that voltage rises (it is a reverse-biased junction capacitance).
BSS806N's datasheet gives COSS at VDS = 10 V (118 pF typical, 169 pF maximum);
this circuit operates at 3.3 V, where COSS is meaningfully higher. Using the
standard first-order approximation COSS(V) ≈ COSS(Vtest) × √(Vtest ⁄ V):

| Part, condition | COSS at datasheet VDS | De-rated COSS at 3.3 V (Estimate) |
|---|---|---|
| BSS806N, typical | 118 pF at 10 V | **≈ 205 pF** |
| BSS806N, maximum | 169 pF at 10 V | ≈ 294 pF |
| IRLML2502, typical (for comparison) | 90 pF at 15 V | ≈ 192 pF |

Adding roughly 20 pF for board trace, the target IC's pin, and probe loading
(**Estimate**, unmeasured) gives a working node capacitance of **about
225 pF** for the calculations below, using BSS806N's typical figure.

## Collapse (turn-on): negligible, driver-limited instead

When the FET turns on, the node discharges through its ~57 mΩ on-resistance
into ~225 pF. That RC time constant is:

```
τ_on = R_DS(on) × C_node ≈ 0.057 Ω × 225 pF ≈ 13 picoseconds
```

This is three orders of magnitude faster than anything else in the signal
path. **The real floor on how fast the node can be pulled down is the gate
driver's own turn-on propagation delay** — 2.6 ns typical, 4.1 ns maximum,
per the LMG1025-Q1 datasheet — not the RC network. This is a materially
different (and much better) conclusion than the earlier decoupling-capacitor
model implied, where the collapse itself was comparable in scale to the
recovery.

## Recovery (release): set by Rs, and now the dominant timescale

When the FET releases, the node recovers toward 3.3 V through Rs into the
same ~225 pF. This time constant is the one actually worth tuning:

```
τ_off = Rs × C_node
rise time (10–90%) ≈ 2.2 × τ_off
```

| Rs | τ_off | Recovery, 10–90% | Crowbar current during glitch | Power in Rs if FET sticks on |
|---|---|---|---|---|
| 1 Ω | 0.23 ns | 0.5 ns | 3.1 A | 10.3 W |
| 4.7 Ω | 1.1 ns | 2.3 ns | 694 mA | 2.3 W |
| 10 Ω | 2.3 ns | 5.0 ns | 328 mA | 1.1 W |
| 22 Ω | 5.0 ns | 10.9 ns | 150 mA | 0.49 W |
| 33 Ω | 7.4 ns | 16.4 ns | 100 mA | 0.33 W |
| 47 Ω | 10.6 ns | 23.3 ns | 70 mA | 0.23 W |
| 100 Ω | 22.5 ns | 49.6 ns | 33 mA | 0.11 W |

(Crowbar current = 3.3 V ⁄ (Rs + RDS(on)); power in Rs if the FET sticks on
uses the same denominator. Both use BSS806N's 57 mΩ maximum.)

## What this means for the sub-20 ns goal

With decoupling removed, **total glitch width is dominated by Rs, with the
driver's own propagation delay (a few nanoseconds) as the practical floor**:

- **Rs in the 10–33 Ω range** keeps the recovery tail between about 5 ns and
  16 ns — comfortably under the sub-20 ns goal, with the delayed-AND method
  ([02-pulse-generation.md](02-pulse-generation.md)) controlling the
  collapse-to-release interval independently, down to the driver's 1.25 ns
  minimum pulse width.
- **Lower Rs** (4.7 Ω and below) gives faster recovery but sharply higher
  crowbar current and stuck-on power — see
  [06-safety-and-protection.md](06-safety-and-protection.md) for why that
  matters.
- **This is a large improvement over the decoupling-capacitor case**, where
  recovery alone would have run to hundreds of nanoseconds or more regardless
  of Rs or pulse timing.

## Parallel footprints for Rs

Because the target IC's real input capacitance and tolerance are unknown
until its part number is available, Rs is laid out as several parallel,
solder-selectable footprints rather than a single fixed value — for example
4.7 Ω, 10 Ω, 22 Ω, and 33 Ω, populated one at a time with a solder jumper or
0-ohm link. This lets the glitch width/crowbar-current trade-off be tuned on
the bench against real measurements instead of being committed to at design
time. Each footprint should be rated for its own stuck-on power (see the
table above) or backed by a fuse — see
[06-safety-and-protection.md](06-safety-and-protection.md).

## Caveats

- This is a first-order, single-pole lumped model. It ignores board and gate
  loop inductance, which will round off edges and can introduce ringing —
  real performance will be slower and noisier than this model predicts,
  especially at the lower Rs values where current changes quickly.
- The COSS de-rating formula is a standard approximation, not a
  manufacturer-specified figure at 3.3 V; treat the ~225 pF node capacitance
  as a planning estimate until measured on a real board.
- None of this accounts for the target IC's own input capacitance or
  on-board bypassing other than its (now-removed) decoupling capacitor —
  unknown until the part number is known.
- Simulate this node (SPICE, in `simulation/`) with the real board parasitics
  before ordering, and confirm with a real measurement once built.
