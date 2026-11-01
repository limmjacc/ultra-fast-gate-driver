# Power and indicator

## Board supply

5 V, intended to come from the BeagleBone Black's own 5 V rail (VDD_5V or
SYS_5V depending on how the BeagleBone itself is powered — see
[05-host-interface.md](05-host-interface.md)) so the driver and the host come
up and down together. The LMG1025-Q1's recommended supply range is
4.75–5.25 V with a 5% stability recommendation from TI; **measure the
BeagleBone's 5 V rail under the driver's actual load before relying on it**
(open item).

## Power-present LED

Any SMD LED is acceptable for this purpose per the project owner. Currently
specified: Würth Elektronik 150060RS75000 (0603, red), driven from the 5 V
rail through a series resistor sized from its forward voltage. Distributor
listings give a 2.4 V forward voltage for this part; the manufacturer's own
datasheet was not retrievable at the time of selection, so this figure is
unconfirmed (see
[../reference/data-reliability.md](../reference/data-reliability.md)). From
5 V at 2.4 V forward voltage, a 1.5 kΩ resistor gives roughly 1.7 mA — enough
for a visible indicator, not a design-critical current.

Keep the LED and its resistor off the driver's own VDD decoupling path (route
them from the 5 V rail before it reaches the driver's local bypass
capacitors) so the LED does not disturb the driver's supply during switching.
