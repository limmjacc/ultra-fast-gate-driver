# Safety and protection

## Scope: what this fixture tests, and what it does not

This board injects a controlled, nanosecond-scale supply dropout into a target
board to study its response to brief glitches and brown-outs. **It is not a
surge-immunity test.** Surge and fast-transient immunity (the kind of testing
referenced by standards like IEC 61000-4-5 for surge, or IEC 61000-4-4 for
electrical fast transient and burst) involves energy levels, source impedances,
and coupling paths this fixture does not reproduce. This fixture is for
exploring glitch and brown-out behaviour on the bench during hobby
reverse-engineering, not a stand-in for formal immunity testing.

## Fixture self-protection

The crowbar deliberately creates a low-impedance path from the target rail to
ground for a brief, controlled interval. If the FET fails on, or the pulse
logic malfunctions and holds it on, that path becomes continuous and Rs carries
full crowbar current until something gives. Because the fixture now handles
rails up to 5.5 V, the stuck-on power is higher than the earlier 3.3 V design:

| Rs | Crowbar current at 3.3 V | at 5.5 V | Continuous power in Rs if stuck on, at 5.5 V |
|---|---|---|---|
| 1 ohm | 3.1 A | 5.2 A | 28.4 W |
| 4.7 ohm | 694 mA | 1.16 A | 6.4 W |
| 10 ohm | 328 mA | 547 mA | 3.0 W |
| 22 ohm | 150 mA | 249 mA | 1.4 W |
| 47 ohm | 70 mA | 116 mA | 0.6 W |

(Current = Vrail / (Rs + RDS(on)), using the BSS806N 57 mohm maximum. Power is
the same denominator into Rs.) The 1 ohm setting at 5.5 V is a short; it must
be fused and used only for the briefest glitches, never relied on to survive a
stuck-on fault.

**Mitigations, in order of priority:**

1. **A hardware maximum on-time**, independent of software and the PRU. A
   one-shot (U3, 74LVC1G123) holds an allowed-window output high for a fixed
   Tmax after each trigger edge; an AND gate (U4, 74LVC1G08) forces the driver
   input low once that window closes, turning the FET off. This works even if
   the PRU hangs with its trigger line high or the delay element fails. It is
   the most important protection in this design. See
   [02-pulse-generation.md](02-pulse-generation.md).
2. **Size Rs's footprint for its stuck-on power at 5.5 V**, or back it with a
   fuse. Use a 1206 or larger footprint for the low values, and do not assume a
   resistor rated for the glitch's average power survives a continuous fault.
3. **Fuse the injection path (F1)**, sized against the stuck-on currents above,
   independent of whatever limit a bench supply or the target provides.
4. **The driver's own protections help but are not sufficient alone:** IN+ has
   an internal 150 kohm pull-down (the gate stays off if the trigger floats or
   the BeagleBone resets), and the driver's UVLO pulls the output low on
   undervoltage. Neither protects against a logic fault that actively commands
   the gate on, which is what the one-shot covers.

## Protecting the target

- **Clamp both directions at the target node.** The SPICE model in
  `simulation/` shows the release rings hard: the supply-path inductance and the
  small node capacitance form a resonant loop, so when the FET releases the node
  undershoots below ground and the energy stored in the supply inductance kicks
  the node back up well above the rail. Both can exceed a target's supply
  absolute maximum (often about -0.3 to -0.5 V on the low side and a few volts
  above the rail on the high side; see [08-target-ic.md](08-target-ic.md) for a
  worked example). A Schottky clamp to ground (D2) catches the undershoot; add a
  high-side clamp as well (a TVS or Schottky to the rail, or a bidirectional
  TVS) for the kickback.
- **Keep Rs moderate and the glitch short.** Lower Rs gives a deeper glitch but
  a larger kickback and more stuck-on current; the simulation suggests starting
  in the 10 to 22 ohm range rather than at the lowest values. A shorter on-pulse
  stores less energy in the supply inductance, so it kicks back less.
- **Keep the loop short.** Ringing on release depends on the lead and loop
  inductance at the target pad. Short clip or solder leads and a nearby ground
  return keep the overshoot and undershoot within the target's absolute maximum.

## Gate overdrive margin

BSS806N's absolute maximum VGS is 8 V against a 5 V nominal drive, a 3 V
overshoot margin that is real but not generous (see
[03-driver-and-fet.md](03-driver-and-fet.md)). Keep the gate loop short and
verify ringing does not exceed this margin before extended testing, especially
at the lower Rs values where edge currents are higher.

## Review

As with any fixture that intentionally stresses another board, review the final
design, including the maximum on-time circuit, Rs sizing and fusing, the clamp,
and the scope note above, before first power-up. This is practical lab
guidance, not a substitute for review by a qualified engineer.
