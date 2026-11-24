# Sourcing

Stock and pricing checked against digikey.ca, for delivery to Edmonton,
Alberta. The active parts below were confirmed in a browser on 2026-11-22
(prices in CAD, single-unit). Still re-confirm stock and price before ordering,
since both move; see [data-reliability.md](data-reliability.md).

## Current BOM

| Ref | Role | Part | Package | digikey.ca (2026-11-22) |
|---|---|---|---|---|
| U1 | Gate driver | TI LMG1025QDEERQ1 | WSON-6 2x2 | In stock, CAD 22.23 |
| Q1 | Crowbar FET | Infineon BSS806NH6327XTSA1 | SOT-23 | In stock, CAD 0.67 |
| U2 | Dual Schmitt buffer | TI SN74LVC2G17DCKR | SC-70-6 | In stock, CAD 0.36 |
| U3 | Monostable (max on-time) | Nexperia 74LVC1G123DP,125 | 8-pin TSSOP | In stock, CAD 0.78 |
| U4 | AND gate (max-on-time gating) | TI SN74LVC1G08DCKR | SC-70-5 | In stock, CAD 0.16 |
| Rs bank | Series crowbar resistor | 1 / 4.7 / 10 / 22 / 47 ohm, power-rated | 1206 or larger | Standard, confirm per value |
| F1 | Injection-path fuse | fast-acting SMD fuse | 1206 | Standard, size per Rs |
| D2 | Negative-ring clamp | Schottky, low Vf, low capacitance | SOD-323 or similar | Standard, pick per note |
| D1, R4 | Power LED and series resistor | Wurth 150060RS75000 + 1.5k | 0603 | In stock |
| J1 | BeagleBone tap | 1x4 header | 2.54 mm | Standard |
| J2 | Optional supply in | 1x2 header | 2.54 mm | Standard |
| target pads, TP1-5 | Target node and scope points | pads / test points | - | Standard |

The resistors, fuse, diode, headers, and test points are commodity parts; pick
exact orderable values during BOM finalisation.

## Manufacturing fields in the schematic

The six confirmed active parts (U1, U2, U3, U4, Q1, D1) carry `Mfr`, `MPN`,
`Supplier`, and `Package` fields on their schematic symbols, so the exported BOM
is orderable without re-sourcing each part by hand. The fields are hidden on the
sheet to keep it clean. The commodity passives and connectors are deliberately
left without an MPN because their exact value is selected per target; fill those
in at BOM finalisation. Export the BOM from the job set (see
[../../hardware/fab-outputs/README.md](../../hardware/fab-outputs/README.md)).

## Notes on specific parts

- **U4 must be an AND (74LVC1G08), not an OR (74LVC1G32).** The max-on-time
  logic forces IN+ low at timeout by ANDing the trigger with the one-shot
  window. The 8-pin 74LVC1G123 exposes only Q, so there is no inverted window to
  OR into IN-. The single-gate DCK package is SC-70-5 (five pins), while the
  dual 2G17 DCK is SC-70-6.
- **U3, 74LVC1G123, is an 8-pin part (TSSOP here), not SOT-23-8.** A SOT-23-8
  version was not found orderable; the 8-pin TSSOP is in stock and fine.
- **U1 price.** The LMG1025-Q1 is an automotive-grade part and the only
  LMG1025 variant; there is no cheaper non-Q option. CAD 22 is expected.

## Alternates and superseded parts

| Role | Part | Status |
|---|---|---|
| Driver, faster alternate | TI LMG1020 (WCSP) | On file only; faster edges but very hard to hand-assemble |
| Delay element, alternate | Data Delay Devices 3D3428 | Programmable 0.25 ns step line; availability unverified, lay out as alternate only |
| FET, superseded | Infineon BSS138N / BSS138W, Diodes BSS138-7-F | Considered under the earlier resistive-load model, before the crowbar topology; not the right part now, see [../design/03-driver-and-fet.md](../design/03-driver-and-fet.md) |

The BSS138 family was selected under the earlier resistive-gate-load model,
before the crowbar application was identified. Once the crowbar topology
replaced that model, BSS806N replaced all three; see
[../decisions/decision-log.md](../decisions/decision-log.md) for the sequence.
