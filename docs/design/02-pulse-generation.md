# Pulse generation

## Why the BeagleBone alone cannot set the glitch width

The AM3358 PRU's direct output mode requires each output phase to be at least
two L3_CLK periods wide (TI datasheet, Table 7-96). If L3_CLK runs at 200 MHz
(**unverified — confirm against the processor documentation before relying on
this**), that is a 5 ns period, giving a 10 ns minimum pulse width in 5 ns
steps. Only 10 ns and 15 ns would fall under the sub-20 ns goal, and with no
resolution finer than 5 ns. A plain Linux GPIO is far too slow and jittery to
use at all for this.

## The delayed-AND method

The LMG1025-Q1 gate driver has two inputs, IN+ and IN-, combined internally
by an AND gate (output goes high when IN+ is high AND IN- is low). The
datasheet (section 7.2.2.2, "Creating Nanosecond Pulse") describes using this
directly as a pulse generator:

> Starting with both IN+ and IN– at low, taking IN+ high will cause the
> output to go high. Now if IN– is taken high as well, output will be pulled
> low. So a digital signal and its delayed version can be applied to IN+ and
> IN– respectively to create a pulse at the output with width corresponding
> to the delay between the signals... The delay can be digitally controlled
> in the nanosecond range.

This is adopted as the primary pulse-generation method:

- **The BeagleBone PRU drives IN+** directly. Its job is only to set *when*
  the glitch happens (the offset), which it can do adequately even at its
  coarse 5–10 ns resolution, since the offset's precision matters far less
  than the width.
- **A delay element on the board derives IN-** from the same edge, delayed by
  the desired glitch width. The driver's datasheet states a 1.25 ns minimum
  input pulse width that changes its output state, so the achievable glitch
  width floor is driver-limited, not BeagleBone-limited.
- Tie IN- low (through its internal 150 kΩ pull-up notwithstanding — drive it
  actively) when not glitching, so the gate stays off between tests.

## Delay element: parallel, solder-selectable footprints

The target IC's part number and real behavior are not yet known, so the delay
element is built to be changed on the bench rather than fixed at design time:

- **Default: RC delay plus a fast buffer**, as the datasheet itself suggests
  ("If a separate delayed version of the digital signal is not available, an
  RC delay followed by a buffer can be used to derive the second signal").
  Populate multiple parallel RC footprints (for example a few values spanning
  roughly 2 ns to 50 ns) with 0-ohm links or solder jumpers to select one
  without a respin.
- **Alternate: a programmable digital delay line**, for repeatable, finer
  steps than discrete RC footprints allow. A search found the Data Delay
  Devices 3D3428 (8-bit, 3.3 V CMOS, 0.25 ns steps per the manufacturer's
  published data), but its current availability is unverified — see
  [../reference/sourcing.md](../reference/sourcing.md). Lay out a footprint
  for this as an alternate population option alongside the RC default, not a
  replacement for it, until it is confirmed orderable.
- **Hard ceiling, independent of the delay element:** a hardware maximum
  on-time (see [06-safety-and-protection.md](06-safety-and-protection.md)) so
  a stuck or misconfigured delay cannot hold the FET on indefinitely.

## Open items

- Confirm the AM3358 L3_CLK frequency (assumed 200 MHz above) against the
  processor documentation, and pick a trigger pin that is a genuine PRU
  direct-output pin, not a boot-strap pin — see
  [05-host-interface.md](05-host-interface.md).
- Choose the actual RC footprint value set once the target IC's required
  glitch-width range is known.
- Confirm the Data Delay Devices part (or an equivalent) is actually
  orderable before committing board space to its footprint.
