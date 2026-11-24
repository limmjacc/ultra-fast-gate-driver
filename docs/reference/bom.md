# Bill of materials

Every line was verified in stock on a live digikey.ca product page on
2026-11-23 (DigiKey Canada, ships to Edmonton AB, prices in CAD, single-unit
Cut Tape). Stock moves quickly, so re-confirm at the moment of ordering; the
MPN and DigiKey part number are the stable keys. These same part numbers are
stored on the schematic symbols (Mfr, MPN, Supplier, Supplier PN, DigiKey Link,
Package, and the Datasheet field), so the job set exports this BOM directly.

Package sizes are metric-imperial as DigiKey lists them: 0603 = 1608 metric,
1206 = 3216 metric.

## Active parts

| Ref | Qty | Value / role | Mfr | MPN | DigiKey PN | In stock (2026-11-23) | CAD @1 | Package |
|---|---|---|---|---|---|---|---|---|
| U1 | 1 | Gate driver | Texas Instruments | LMG1025QDEERQ1 | 296-LMG1025QDEERQ1CT-ND | 755 | 22.23 | WSON-6 |
| U2 | 1 | Dual Schmitt buffer | Texas Instruments | SN74LVC2G17DCKR | 296-13013-1-ND | 2,158 | 0.36 | SC-70-6 |
| U3 | 1 | Monostable (max on-time) | Nexperia | 74LVC1G123DP,125 | 1727-2238-1-ND | 17,156 | 0.78 | TSSOP-8 |
| U4 | 1 | AND gate (max-on-time gating) | Texas Instruments | SN74LVC1G08DCKR | 296-11602-1-ND | 539,794 | 0.16 | SC-70-5 |
| Q1 | 1 | Crowbar FET | Infineon | BSS806NH6327XTSA1 | BSS806NH6327XTSA1CT-ND | 193,468 | 0.67 | SOT-23 |

## Diodes

| Ref | Qty | Value / role | Mfr | MPN | DigiKey PN | In stock (2026-11-23) | CAD @1 | Package |
|---|---|---|---|---|---|---|---|---|
| D1 | 1 | Power LED (red) | Wurth Elektronik | 150060RS75000 | 732-4978-1-ND | 237,979 | 0.24 | 0603 |
| D2 | 1 | Node clamp, low side (undershoot) | Comchip Technology | RB751V-40 | 641-1943-1-ND | 4,834 | 0.43 | SOD-323 |
| D3 | 1 (DNP) | Node clamp, high side (kickback) | Comchip Technology | RB751V-40 | 641-1943-1-ND | 4,834 | 0.43 | SOD-323 |

## Fuse

| Ref | Qty | Value / role | Mfr | MPN | DigiKey PN | In stock (2026-11-23) | CAD @1 | Package |
|---|---|---|---|---|---|---|---|---|
| F1 | 1 | Injection-path fuse, fast, 1 A, 125 V | Littelfuse | 0470001.DRSNP | F6623CT-ND | 8,616 | 2.87 | 1206 |

## Resistors

| Ref | Qty | Value / role | Mfr | MPN | DigiKey PN | In stock (2026-11-23) | CAD @1 | Package |
|---|---|---|---|---|---|---|---|---|
| R1, R2 | 2 | 4.7 ohm, gate series (OUTH/OUTL) | Yageo | RC0603JR-074R7L | 311-4.7GRCT-ND | 561,454 | 0.17 | 0603 |
| R5 | 1 | 100 ohm, glitch-width RC delay | Panasonic | ERJ-3EKF1000V | P100HCT-ND | 2,284,669 | 0.16 | 0603 |
| R6 | 1 | 10 kohm, max-on-time RC | Stackpole | RMCF0603FT10K0 | RMCF0603FT10K0CT-ND | 5,958,194 | 0.17 | 0603 |
| R4 | 1 | 1.5 kohm, LED series | Yageo | RC0603FR-071K5L | 311-1.50KHRCT-ND | 261,056 | 0.16 | 0603 |
| R7 | 1 (DNP) | 0 ohm, optional supply link | Yageo | RC0603JR-070RL | 311-0.0GRCT-ND | 7,297,437 | 0.16 | 0603 |
| R3_1 | 1 | 1 ohm, Rs crowbar bank | Yageo | RC1206FR-071RL | 311-1.00FRCT-ND | 207,689 | 0.27 | 1206 |
| R3_2 | 1 | 4.7 ohm, Rs crowbar bank | Yageo | RC1206FR-074R7L | 311-4.70FRCT-ND | 70,694 | 0.27 | 1206 |
| R3_3 | 1 | 10 ohm, Rs crowbar bank | Yageo | RC1206FR-0710RL | 311-10.0FRCT-ND | 197,512 | 0.27 | 1206 |
| R3_4 | 1 | 22 ohm, Rs crowbar bank | Yageo | RC1206FR-0722RL | 311-22.0FRCT-ND | 194,882 | 0.19 | 1206 |
| R3_5 | 1 | 47 ohm, Rs crowbar bank | Yageo | RC1206FR-0747RL | 311-47.0FRCT-ND | 86,054 | 0.17 | 1206 |

## Capacitors

| Ref | Qty | Value / role | Mfr | MPN | DigiKey PN | In stock (2026-11-23) | CAD @1 | Package |
|---|---|---|---|---|---|---|---|---|
| C1 | 1 | 0.1 uF X7R 16 V, 3V3 bypass | Yageo | CC0603KRX7R7BB104 | 311-1088-1-ND | 3,796,242 | 0.21 | 0603 |
| C2 | 1 | 1 uF X7R 16 V, 5 V bypass | Yageo | CC0603KRX7R7BB105 | 311-1446-1-ND | 3,417,801 | 0.36 | 0603 |
| C3 | 1 | 100 pF C0G 50 V, glitch-width RC | Samsung Electro-Mechanics | CL10C101JB8NNNC | 1276-1008-1-ND | 1,362,613 | 0.15 | 0603 |
| C4 | 1 | 1 nF C0G 50 V, max-on-time RC | KEMET | C0603C102F5GACTU | 399-C0603C102F5GACTUCT-ND | 85,829 | 2.63 | 0603 |

## Connectors

| Ref | Qty | Value / role | Mfr | MPN | DigiKey PN | In stock (2026-11-23) | CAD @1 | Package |
|---|---|---|---|---|---|---|---|---|
| J1 | 1 | BeagleBone tap, 1x4 | Sullins | PRPC004SAAN-RC | 35-PRPC004SAAN-RC-ND | 5,404 | 0.15 | 2.54 mm header |
| J2 | 1 | Optional supply in, 1x2 | Sullins | PRPC002SAAN-RC | 35-PRPC002SAAN-RC-ND | 108,288 | 0.15 | 2.54 mm header |
| J3 | 1 | Target pads, 1x2 | Sullins | PRPC002SAAN-RC | 35-PRPC002SAAN-RC-ND | 108,288 | 0.15 | 2.54 mm header |

## Not ordered (board features)

TP1 to TP5 are scope test points realised as PCB pads or wire loops; there is no
part to purchase. Add Keystone loop test points at layout only if you want
physical loops.

## Approximate one-off cost

About CAD 34 at single-unit pricing, dominated by U1 (the LMG1025-Q1, roughly
CAD 22, the only LMG1025 variant and automotive grade). Everything else totals
around CAD 12. Prices fall sharply at higher quantities on every line.

## Selection notes and caveats

- **Rs bank power rating.** The 1206 resistors are 1/4 W continuous. They are
  sized for the nanosecond glitch pulse, not for a stuck-on fault; the low
  values (1 and 4.7 ohm) would exceed their continuous rating if the FET stuck
  on. The fuse F1 and the hardware max-on-time one-shot are what protect against
  that case. See [../design/06-safety-and-protection.md](../design/06-safety-and-protection.md).
- **D2 and D3 are low-capacitance Schottkys on purpose.** The clamp sits on the
  glitch node (about 225 pF total), so a low-capacitance part matters; the
  RB751V-40 adds only about 2 pF. Its 30 V / 30 mA rating is fine because the
  clamp only catches the brief, low-energy ring on release. A higher-current
  Schottky such as the Toshiba CUS10S30 is in stock too but adds about 135 pF,
  which would load the node, so it is not the first choice. The low-capacitance
  Nexperia PMEG2010EA is the ideal part electrically but was backorder-only on
  2026-11-23.
- **D3 is the same part as D2**, fitted only if the high-side kickback clamp is
  wanted (it is DNP by default). The low-capacitance Littelfuse SMF6.0CA TVS
  that the design text mentions as an alternative was backorder-only on
  2026-11-23, so a Schottky-to-rail is the stocked choice; see
  [../design/06-safety-and-protection.md](../design/06-safety-and-protection.md).
- **Timing parts (R5, C3, R6, C4) are starting values**, chosen so the glitch
  width and the max-on-time one-shot land in sensible ranges. Tune R5/C3 for the
  target's needed glitch width and R6/C4 for the max-on-time backstop; the
  footprints are solder-selectable. C3 and C4 are C0G for timing stability. The
  1 nF C0G (C4) is the one pricey passive (CAD 2.63); a plain X7R 1 nF works
  for the max-on-time backstop if you want to save a couple of dollars, since
  that time constant is not precision critical.
- **Tolerances.** Most resistors are 1 percent. The 4.7 ohm 0603 (R1, R2) is 5
  percent, because no 1 percent 4.7 ohm 0603 was stocked on digikey.ca; 5
  percent is fine for a gate series resistor.
- **J2 and J3 use the same 1x2 header.** J3 (the target connection) can also be
  short soldered jumper wires straight onto the target rail instead of a header.

Verification method: each digikey.ca product page was opened and its live
In-Stock figure read directly, not taken from a third-party aggregator.
