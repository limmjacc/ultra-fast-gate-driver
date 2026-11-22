# Pulse generation

## The signal chain

```
PRU trigger ─▶ U2A buffer ─▶ TRIG_B ─┬─▶ U4 AND ─▶ IN+   (direct path)
                                     ├─▶ RC delay ─▶ U2B buffer ─▶ IN-  (delayed path)
                                     └─▶ U3 one-shot ─▶ Q window ─▶ U4 AND (max on-time)
```

A single logic buffer squares the PRU edge and feeds two paths. The direct
path sets when the glitch starts; the delayed path sets how wide it is. A
one-shot gates the direct path so the glitch cannot run longer than a fixed
maximum.

## Why the BeagleBone alone cannot set the glitch width

The AM3358 PRU's direct output mode requires each output phase to be at least
two L3_CLK periods wide (TI datasheet, Table 7-96). If L3_CLK runs at 200 MHz
(**unverified, confirm against the processor documentation before relying on
this**), that is a 5 ns period, giving a 10 ns minimum pulse in 5 ns steps.
That is fine for setting the glitch's timing offset, but too coarse to set the
width directly. A plain Linux GPIO is far too slow and jittery to use at all.

## The input buffer

A 74LVC2G17 dual Schmitt-trigger buffer (U2) sits between the PRU and the rest
of the board. It does two jobs:

- **Squares the edge** so the downstream timing does not depend on the PRU
  edge shape.
- **Guarantees the drive level.** The gate driver's IN+ is high above 2.6 V
  maximum. The PRU alone clears that by only about 85 mV at its rated test
  current (see [05-host-interface.md](05-host-interface.md)); running it
  through a 3V3 buffer whose output swings to the rail removes that worry.

One buffer channel drives the direct path (IN+), the other re-squares the
RC-delayed signal before it reaches IN-.

## The delayed-AND method for glitch width

The LMG1025-Q1 gate driver has two inputs, IN+ and IN-, combined internally by
an AND gate (the output is high when IN+ is high and IN- is low). The datasheet
(section 7.2.2.2, "Creating Nanosecond Pulse") describes using this as a pulse
generator: take IN+ high, then take IN- high a short time later, and the output
is a pulse whose width equals the delay.

- **The direct path drives IN+** (through the max-on-time AND gate, below).
- **An RC delay plus the second buffer derives IN-** from the same edge,
  delayed by the desired glitch width. The driver's datasheet gives a 1.25 ns
  minimum input pulse width, so the glitch-width floor is driver-limited, not
  BeagleBone-limited.

### Delay element: parallel, solder-selectable footprints

The target board and its real behaviour are not known in advance, so the delay
is built to be changed on the bench:

- **Default: an RC delay followed by the buffer**, as the datasheet suggests.
  Populate parallel RC footprints (for example values spanning roughly 2 ns to
  50 ns) and select one with a solder jumper, so the width can be tuned without
  a respin.
- **Alternate: a programmable digital delay line** for repeatable fine steps.
  A candidate is the Data Delay Devices 3D3428 (8-bit, 3.3 V CMOS, 0.25 ns
  steps per the manufacturer's data), availability unverified; see
  [../reference/sourcing.md](../reference/sourcing.md). Lay out its footprint
  as an alternate, not a replacement for the RC default, until confirmed
  orderable.

## Max on-time gating

A hardware one-shot (U3, 74LVC1G123 monostable) is triggered by the same
squared edge and holds its Q output high for a fixed window Tmax, set by an
external Rmt and Cmt. An AND gate (U4, 74LVC1G08) forms IN+ as the direct
trigger ANDed with Q. After Tmax the window closes and IN+ is forced low, so
the driver output goes low and the FET turns off, regardless of what the
trigger or the delay element does. This is the primary protection and does not
depend on the BeagleBone continuing to run correctly; see
[06-safety-and-protection.md](06-safety-and-protection.md).

The 8-pin 74LVC1G123 exposes only Q (no inverted output), which is why the
gate is an AND on IN+ (forcing the pulse off at timeout) rather than an OR on
IN-. Between glitches, with the trigger low, IN+ is low and the FET is off.

## Open items

- Confirm the AM3358 L3_CLK frequency (assumed 200 MHz above) against the
  processor documentation, and pick a trigger pin that is a genuine PRU
  direct-output pin, not a boot-strap pin; see
  [05-host-interface.md](05-host-interface.md).
- Match the propagation delays of the IN+ and IN- paths. The AND gate adds a
  gate delay to IN+ that the IN- path should match, so it does not eat into the
  minimum achievable width. Confirm on the bench.
- Choose the RC footprint value set once a target's required glitch-width range
  is known.
- Confirm the Data Delay Devices part (or an equivalent) is orderable before
  committing board space to its footprint.
