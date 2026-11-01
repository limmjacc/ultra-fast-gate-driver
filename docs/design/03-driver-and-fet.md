# Driver and FET selection

Full datasheet figures are in
[../reference/datasheet-notes.md](../reference/datasheet-notes.md); this
document is the reasoning that led to the current selection. Both datasheets
are saved in `hardware/datasheets/`.

## Gate driver: TI LMG1025-Q1

**Selected.** WSON 2×2 mm (hand-reflowable), 5 V supply, 7 A source / 5 A
sink, 2.6 ns / 2.9 ns typical turn-on / turn-off propagation delay, 650 ps /
850 ps edges into a 220 pF load, 1.25 ns minimum input pulse width. Its
two-input AND-gate structure is also the basis of the pulse-generation method
in [02-pulse-generation.md](02-pulse-generation.md).

- **Accepts the BeagleBone's 3.3 V logic, with a real but narrow margin.**
  VIH is 2.6 V maximum; the AM3358 guarantees at least 2.685 V from a pin
  sourcing 4 mA (worst-case VDDSHV of 3.135 V minus a 0.45 V drop). The margin
  is about 85 mV at full rated current, though the actual load the driver
  input presents (a 150 kΩ pull-down, drawing tens of microamps) means the
  real output should sit closer to the rail. See
  [05-host-interface.md](05-host-interface.md).
- **5 V supply has a narrow range.** Recommended 4.75–5.25 V, absolute
  maximum 5.75 V, with TI recommending the supply be held within 5%. Measure
  the BeagleBone's 5 V rail under the driver's actual load before relying on
  it — see [07-power-and-indicator.md](07-power-and-indicator.md).
- **Not characterized above 30 MHz continuous.** This matters for how often
  the fixture can repeat glitches, not for a single glitch's speed. TI's own
  guidance (section 7.2.2.4) is to burst rather than run continuously at high
  repetition rates.
- **Alternate on file, not currently selected:** TI LMG1020, a 0.8×1.2 mm
  WCSP with even faster edges (400 ps typical). Rejected for now because the
  package is very difficult to hand-assemble; keep as an upgrade path if the
  LMG1025-Q1's edges prove insufficient once measured.

## FET: Infineon BSS806N

**Selected**, replacing an earlier BSS138N/BSS138-7-F selection that assumed
a resistive gate-load application (see
[../decisions/decision-log.md](../decisions/decision-log.md), entries 2–7).

In a crowbar, the figures that matter are low on-resistance (to pull the node
close to ground), low gate charge (so the driver turns it on fast), and low
output capacitance (it adds directly to the node capacitance the recovery
math in [04-timing-and-recovery.md](04-timing-and-recovery.md) depends on) —
not drain-edge speed into a fixed resistive load, which was the old model.

| Part | RDS(on) | Qg | COSS (datasheet condition) | VGS max | Pulsed ID |
|---|---|---|---|---|---|
| **BSS806N (selected)** | 41 mΩ typ / 57 mΩ max at VGS 2.5 V | 1.7 nC | 118 pF typ / 169 pF max at VDS 10 V | 8 V | 9.3 A |
| IRLML2502 (considered, not selected) | 35 mΩ typ / 45 mΩ max at VGS 4.5 V | 8 nC | 90 pF typ at VDS 15 V | 12 V | 33 A |

BSS806N's lower gate charge means the driver turns it on faster for a given
drive current (**Estimate**: roughly a nanosecond at the driver's rated
current), and its output capacitance, once de-rated to the circuit's actual
3.3 V, is comparable to IRLML2502's — see
[04-timing-and-recovery.md](04-timing-and-recovery.md) for that de-rating and
why it matters. IRLML2502's much higher pulsed-current rating is not needed
here; the crowbar current estimated for realistic Rs values is well under 1 A
(see the same document).

**Gate voltage margin is tighter than it looks.** BSS806N's absolute maximum
VGS is 8 V. The 5 V drive leaves 3 V of overshoot headroom — adequate, but
tighter than a part rated for ±20 V. Keep the gate loop short and tune the
driver's OUTH series resistor to control ringing (see the layout guidance in
[../reference/datasheet-notes.md](../reference/datasheet-notes.md)); do not
assume the full 8 V is free margin once real board parasitics are in the
loop.

**Stock status:** see [../reference/sourcing.md](../reference/sourcing.md).
As of the last check, BSS806N showed as active and in stock at digikey.ca,
though that figure came from a page-summary tool and should be re-confirmed
in a browser before ordering.
