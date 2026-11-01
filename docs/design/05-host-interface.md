# Host interface: BeagleBone Black

Figures below are read from the AM3358 processor datasheet (SPRS717L) and the
BeagleBoard.org BeagleBone Black manual, both saved in `hardware/datasheets/`.
See [../reference/datasheet-notes.md](../reference/datasheet-notes.md) for
the full extracted table.

## Logic levels

The AM3358's 3.3 V I/O buffers guarantee VOH of at least VDDSHV − 0.45 V at
4 mA, with VDDSHV specified from 3.135 V to 3.465 V. Worst case, that is
**2.685 V**, against the LMG1025-Q1's 2.6 V maximum VIH — a margin of about
85 mV at the datasheet's test current. The driver input only presents a
150 kΩ pull-down, drawing a few tens of microamps, so the real output voltage
should sit closer to the unloaded rail than the 4 mA test condition implies,
but this has not been measured. VIL is comfortably compatible (AM3358 0.8 V
maximum versus driver 1.1 V minimum).

## Rail limits and board protection

- All BeagleBone expansion header signals are 3.3 V; the manual states
  explicitly that 5 V logic will damage the board, and that no voltage may be
  applied to any I/O pin while the board is unpowered.
- P9 power pins: VDD_3V3B at 250 mA per pin, VDD_5V at 1000 mA per pin (only
  present when powered from the DC jack), SYS_5V at 250 mA (the only 5 V rail
  available when powered from USB, limited further by the USB port's 500 mA
  total).
- The driver's own current draw (75 µA quiescent, roughly 40–51 mA while
  switching at up to the characterized 30 MHz) fits easily within either
  rail.

## Trigger pin selection

- **Use a genuine PRU direct-output pin**, not a plain Linux GPIO, for
  anything timing-critical — see [02-pulse-generation.md](02-pulse-generation.md)
  for why.
- **Avoid the sixteen boot-strap pins** exposed on the expansion headers; the
  manual warns these must not be driven at power-up, since doing so can
  change the processor's boot mode.
- Confirm the specific pin and its PRU mux setting in the manual before
  finalizing the schematic (open item).

## Timing resolution (carried forward from the 48 MHz investigation)

The PRU's direct output mode requires each output phase to be at least two
L3_CLK periods wide. If L3_CLK runs at 200 MHz (**unverified against the
processor documentation**), that is a 5 ns period and a 10 ns minimum pulse
in 5 ns steps — adequate for setting the glitch's *timing offset*, which is
what the PRU is used for in this design, but not for setting glitch *width*
directly (see [02-pulse-generation.md](02-pulse-generation.md), which hands
width off to an on-board delay element instead).

## Grounding

The BeagleBone, this board, and the target IC's board share one logic
ground — see [01-topology.md](01-topology.md) and
[../reference/isolation-analysis.md](../reference/isolation-analysis.md).
Tie the trigger signal ground to the FET source return at a single point near
the FET, per the driver datasheet's ground-bounce guidance, rather than
relying on a shared plane alone.
