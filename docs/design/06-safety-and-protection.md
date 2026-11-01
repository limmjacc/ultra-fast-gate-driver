# Safety and protection

## Scope: what this fixture tests, and what it does not

This board injects a controlled, nanosecond-scale supply dropout into a
target IC to test tolerance to brief transients and brown-outs. **It is not a
lightning-surge immunity test.** Surge and fast-transient immunity (the kind
of testing referenced by standards like IEC 61000-4-5 for surge, or
IEC 61000-4-4 for electrical fast transient/burst) involves energy levels,
source impedances, and coupling paths this fixture does not reproduce — it is
a different, much more involved test setup. This fixture is for exploring
glitch and brown-out behavior on the bench, not a stand-in for that kind of
formal immunity testing.

## Fixture self-protection

The crowbar deliberately creates a low-impedance path from the supply to
ground for a brief, controlled interval. If the FET fails on, or the pulse
logic malfunctions and holds it on, that path becomes continuous, and Rs
(see [04-timing-and-recovery.md](04-timing-and-recovery.md)) is left carrying
full crowbar current indefinitely:

| Rs | Crowbar current | Continuous power in Rs if stuck on |
|---|---|---|
| 1 Ω | 3.1 A | 10.3 W |
| 4.7 Ω | 694 mA | 2.3 W |
| 10 Ω | 328 mA | 1.1 W |
| 22 Ω | 150 mA | 0.49 W |

A higher-current, current-limited bench supply (an acceptable way to remove
"supply capacity" as a constraint on the glitch itself, per the project
owner) makes this worse, not better, if a current limit is set above what Rs
and the FET can dissipate continuously — the supply will happily sustain a
stuck-on fault rather than folding back.

**Mitigations, in order of priority:**

1. **A hardware maximum on-time**, independent of software or the PRU, that
   force-releases the FET after a fixed short interval regardless of what the
   trigger logic does. This is the most important protection in this design
   and should not depend on the BeagleBone continuing to run correctly.
2. **Size Rs's footprint for its stuck-on power**, or back it with a fuse —
   do not assume a 0603 resistor rated for the glitch's average power is
   adequate for a continuous fault.
3. **Fuse or current-limit the 3V3 feed itself**, sized against the
   stuck-on currents above, independent of whatever limit the bench supply
   provides.
4. **The driver's own protections help but are not sufficient alone:** IN+
   has an internal 150 kΩ pull-down (gate stays off if the trigger input
   floats or the BeagleBone resets/loses power), and the driver's UVLO pulls
   OUTL low on an undervoltage fault. Neither protects against a logic fault
   that actively commands the gate on.

## Gate overdrive margin

BSS806N's absolute maximum VGS is 8 V against a 5 V nominal drive — a 3 V
overshoot margin that is real but not generous (see
[03-driver-and-fet.md](03-driver-and-fet.md)). Keep the gate loop short and
verify ringing does not exceed this margin before extended testing,
especially at the lower Rs footprint values where edge currents are higher.

## Review

As with any test fixture that will be used against (and potentially stress)
a real IC, review the final design — including the maximum on-time
protection, Rs sizing, and the fuse/current-limit plan — before first
power-up. This is engineering guidance, not a substitute for that review.
