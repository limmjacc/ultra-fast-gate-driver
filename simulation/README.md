# Simulation

First-order SPICE model of the crowbar node, used to check the hand analysis in
[../docs/design/04-timing-and-recovery.md](../docs/design/04-timing-and-recovery.md)
before committing to a PCB layout.

## Files

- `crowbar-node.cir` - the SPICE deck. Run with `ngspice -b crowbar-node.cir`
  (ngspice is also built into KiCad's simulator). It writes one data file per
  run into this folder.
- `plot_results.py` - reads the data files and writes the two PNGs below. Needs
  numpy and matplotlib.
- `crowbar-node-rs-sweep.png` - target node voltage over time for Rs = 1, 4.7,
  10, 22, 47 ohm, decoupling removed.
- `crowbar-node-decoupling.png` - target node voltage with the local decoupling
  removed versus left in place, at Rs = 10 ohm.

## What the model is

The target supply `Vrail` reaches the injection node through its supply-path
resistance `Rsrc` and inductance `Lsrc`. The node has capacitance `Cnode` (local
decoupling removed). The FET is an ideal voltage-controlled switch with the
BSS806N on-resistance, in series with `Rs`. The gate is driven by a 10 ns pulse.

The parameters at the top of the deck are meant to be changed per target:
`VR` (rail voltage up to 5.5), `RSRC` and `LS` (how stiff and how inductive the
target's supply path is at nanosecond timescales), `CN` (node capacitance with
decoupling removed), and `CDEC` (any decoupling left on the node).

## What it shows

1. **Removing the local decoupling is what makes a glitch possible.** With a
   100 nF decoupling cap left on the node, the rail does not move (flat line at
   3.3 V). With it removed, the small node capacitance collapses in a few
   nanoseconds. This confirms the project's central decision.

2. **Rs sets glitch depth and damping.** Lower Rs pulls the node deeper during
   the on-pulse (Rs = 1 ohm reaches ground; Rs = 47 ohm only dips to about
   1.8 V), but lower Rs also means higher current and worse ringing.

3. **The release rings, and can swing past the target's absolute maximums in
   both directions.** The supply-path inductance and the node capacitance form a
   resonant loop with little natural damping. When the FET releases, the energy
   stored in `Lsrc` dumps into `Cnode` and the node overshoots well above the
   rail (inductive kickback) and then undershoots below ground. In this
   idealized model the swing is large (Rs = 1 ohm overshoots past +11 V and
   undershoots below -4 V from a 3.3 V rail). A real board has more loss and
   will ring less, but the direction of the lesson is firm.

## Consequences for the design

- **Clamp both directions at the target node, not just the negative side.** The
  current design has a Schottky clamp to ground for the undershoot; the
  overshoot on release needs a clamp too (a TVS or Schottky to the rail, or a
  bidirectional TVS), sized to the target's supply absolute maximum. Tracked in
  [../docs/open-items.md](../docs/open-items.md).
- **Do not use the lowest Rs values for sustained or wide glitches.** Low Rs
  gives the deepest glitch but the worst kickback and the highest stuck-on
  current. Rs in the 10 to 22 ohm range is a better starting point; tune per
  target.
- **Keep the glitch short.** Less current builds in the supply inductance during
  a short on-pulse, so the release kickback is smaller.

## Caveats

This is a first-order, idealized model. It uses an ideal switch, a lumped node
capacitance, and an assumed supply-path inductance (50 nH); it ignores
gate-loop inductance, board parasitics, and the FET's real nonlinear
capacitance. Treat the numbers as directional, re-run with values measured on
the actual target board, and confirm against a real measurement once built.
