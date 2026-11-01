# Does the trigger input need isolation?

**Conclusion: no, not for this design as described.** This is an engineering
starting point and needs review by a qualified engineer. It depends on two
assumptions the project owner confirmed: the 3V3 target rail shares the
host's ground, and no hazardous voltage appears anywhere in the system.

## Reasons

1. **There is no voltage to isolate.** The FET crowbars a 3V3 rail with its
   source at 0 V, and the driver is powered from the BeagleBone's own 5 V.
   The trigger and the driver already share the BeagleBone's ground. The
   driver datasheet itself assumes the driver's ground returns directly to
   the FET's source.
2. **Isolators cost more delay than the whole speed budget.** Delays found on
   published datasheets: ADuM110N up to 13 ns maximum; Si8610 5–13 ns;
   ISO7721 11 ns typical / 17 ns maximum, with several ns of additional skew.
   The LMG1025-Q1's own propagation delay is 2.6–2.9 ns typical, and the
   target edge/glitch timing is in the same range — an isolator would add
   more delay than the entire target.
3. **Isolation needs an isolated supply** for the driver side and adds board
   area and a second ground domain, working against the compact, low-
   inductance gate loop the driver datasheet requires.

## Real risks and mitigations (from the datasheets)

- **Ground bounce.** The LMG1025-Q1 datasheet (section 7.2) recommends a
  single tie point between signal ground and the FET source, an RC filter on
  the input for moderate cases, and notes the added delay is acceptable when
  pulses are not near 1 ns. Put a small series resistor at the trigger input.
- **Host protection.** The BeagleBone's I/O is not 5 V tolerant and must not
  be driven while the board is unpowered. Power this board from the
  BeagleBone's own rail so both come up and down together, and keep the
  series resistor at the input. The driver's IN+ pull-down keeps the gate off
  if the pin floats.
- **Boot pins.** Do not use a BeagleBone pin that is driven at boot as the
  trigger — see [../design/05-host-interface.md](../design/05-host-interface.md).

## When isolation would become necessary

- The 3V3 target rail has a different ground reference from the host, or
  floats.
- Any hazardous or high voltage appears anywhere on the target side.
- A long cable carries the trigger between separately powered units. In that
  case, use a differential signal or a fast isolator and accept the added
  delay this analysis shows that would cost.
