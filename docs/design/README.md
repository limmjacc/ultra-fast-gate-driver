# Design

How the circuit works and why, organized by subsystem. Read in order if new
to the project; jump directly to a section if looking something up. For *how
the design got here* rather than *what it currently is*, see
[../decisions/decision-log.md](../decisions/decision-log.md).

1. [Topology](01-topology.md) — the crowbar circuit, block diagram, grounding
2. [Pulse generation](02-pulse-generation.md) — the delayed-AND method, the
   BeagleBone's role, parallel footprints for the delay element
3. [Driver and FET](03-driver-and-fet.md) — part selection and the electrical
   reasoning behind it
4. [Timing and recovery](04-timing-and-recovery.md) — the RC math that sets
   achievable glitch width, and the parallel Rs footprint plan
5. [Host interface](05-host-interface.md) — BeagleBone Black specifics: logic
   levels, PRU timing, pin selection, grounding
6. [Safety and protection](06-safety-and-protection.md) — stuck-on protection,
   maximum on-time, current limiting, and what this fixture is (and is not) a
   test of
7. [Power and indicator](07-power-and-indicator.md) — the 5 V board supply and
   the power-present LED
8. [Target IC: CY8C4125](08-target-ic.md) — the target part's power system,
   why its own internal regulator matters, and a part-number ambiguity that
   needs confirming

Every document here states its assumptions and marks anything derived rather
than read from a datasheet as **Estimate**. None of this has been built,
simulated, or measured yet — see [../open-items.md](../open-items.md).
