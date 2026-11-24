# Requirements

See [decisions/decision-log.md](decisions/decision-log.md) for how these were
arrived at, including requirements that were stated and then superseded.

## Purpose

Pull a target board's supply rail down to ground for a controlled,
nanosecond-scale duration, then release it, to study how a microcontroller
responds to brief supply glitches. The fixture is general-purpose: it is meant
for old, dead, or scrap microcontroller boards found during hobby
reverse-engineering, not for one specific part. See
[design/06-safety-and-protection.md](design/06-safety-and-protection.md) for
what this does and does not test (it is not a surge-immunity test).

## Fixed

- **Trigger input:** from a BeagleBone Black PRU, 3V3 logic, active high. The
  PRU gives a deterministic, low-jitter edge; see
  [design/05-host-interface.md](design/05-host-interface.md).
- **Target rail voltage:** up to 5.5 V, covering 1.8, 2.5, 3.3, and 5 V
  parts. Rs power ratings and protection are sized for the 5.5 V worst case;
  see [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md) and
  [design/06-safety-and-protection.md](design/06-safety-and-protection.md).
- **Injection:** the fixture crowbars the target's own live rail. The FET and
  a series resistor Rs clip or solder with short leads onto the target rail.
  An optional self-supply footprint lets the fixture source the rail instead,
  when wanted. See [design/01-topology.md](design/01-topology.md).
- **Grounding:** the BeagleBone, this board, and the target board share one
  logic ground. No isolation required; see
  [reference/isolation-analysis.md](reference/isolation-analysis.md).
- **Node capacitance:** kept small by working at the target's own supply pin
  and desoldering the local decoupling there, so the node is a few millimetres
  of copper plus the FET output capacitance. See
  [design/04-timing-and-recovery.md](design/04-timing-and-recovery.md).
- **Glitch width:** short and tunable. Set by the driver's delayed-AND method
  with a solder-selectable RC delay, down to the driver's own minimum pulse
  width. See [design/02-pulse-generation.md](design/02-pulse-generation.md).
- **Pulse generation:** a logic buffer squares the PRU edge and feeds the
  driver's IN+ and a delayed IN-. See
  [design/02-pulse-generation.md](design/02-pulse-generation.md).
- **Max on-time protection:** an independent hardware one-shot limits how long
  the FET can be on, regardless of the trigger or the delay logic. See
  [design/06-safety-and-protection.md](design/06-safety-and-protection.md).
- **Board supply:** 5 V for the driver and 3V3 for the logic, both from the
  BeagleBone.
- **Rs bank:** solder-selectable 1, 4.7, 10, 22, 47 ohm, one populated at a
  time, each footprint rated for its stuck-on power at 5.5 V.
- **Power-present indicator:** an SMD LED.
- **Test points:** on the trigger, IN+, IN-, gate, and target node, for scope
  access with a short ground return.

## Open

| Parameter | Status |
|---|---|
| Target rail's real node capacitance once decoupling is removed | Estimated from the FET's COSS; depends on the specific board. Small nodes (a few mm of copper) are the design assumption |
| Glitch depth/duration sweep | The board keeps both knobs adjustable (Rs and the delay element); the sweep test code is written separately |
| Delay-element value set | Parallel RC footprints (roughly 2 to 50 ns span); exact values chosen per target on the bench |
| Max on-time value | R6/C4 set it; pick a value well above the intended glitch but short enough to protect Rs |
| Bench supply current limit (self-supply mode) | Set deliberately against the stuck-on table in [design/06-safety-and-protection.md](design/06-safety-and-protection.md) |
| Form factor and connectors | Header and pad choices pending layout |
| Number of channels | One |

See [open-items.md](open-items.md) for the full working checklist.
