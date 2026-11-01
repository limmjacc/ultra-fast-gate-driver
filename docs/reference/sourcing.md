# Sourcing

Stock and pricing checked against digikey.ca, for delivery to Edmonton,
Alberta. Most figures below came from a page-fetch tool that returns a
model-generated summary of the page rather than its verbatim text (see
[data-reliability.md](data-reliability.md)), and search-snippet figures
disagreed with page-fetch figures more than once during this project.
**Confirm every quantity and price in a browser before ordering.**

| Role | Part | digikey.ca status (last checked 2026-11-01) | Decision |
|---|---|---|---|
| Gate driver | TI LMG1025QDEERQ1 (WSON 2×2, automotive) | 883 in stock, CAD 20.98 each (cut tape), 20-week lead time on backorder | Selected |
| Gate driver, alternate packaging | TI LMG1025QDEETQ1 | 2,151 in stock, CAD 22.46 each, 26-week lead time | Use if DEERQ1 sells out |
| MOSFET (crowbar) | Infineon BSS806N (BSS806NH6327XTSA1, SOT-23) | ~218,890 reported in stock (unconfirmed, see note above), CAD 0.67, Active, 26-week lead time on backorder | **Selected** — see [../design/03-driver-and-fet.md](../design/03-driver-and-fet.md) |
| MOSFET, superseded (resistive-load model) | Infineon BSS138N (BSS138NH6327XTSA2) | 0 in stock, 48-week lead time, CAD 0.55 | Not orderable; not needed under current topology |
| MOSFET, superseded (in-stock substitute) | Diodes BSS138-7-F (SOT-23) | 2,503,836 in stock, CAD 0.34 | Not needed under current topology |
| MOSFET, superseded alternate | Infineon BSS138W (SOT-323) | 0 in stock, 41-week lead time | Not needed under current topology |
| Power LED | Würth 150060RS75000 (0603 red) | ~282,898 in stock (page-fetch summary), CAD 0.24 | Selected |
| Driver, faster alternate | TI LMG1020YFFR | 0 in stock, 3,000 units expected 2026-11-17 | On file as an upgrade path only |
| Pulse-width delay element, alternate | Data Delay Devices 3D3428 (0.25 ns step programmable delay line) | Not checked — no distributor listing found during this project | Unverified; see [../design/02-pulse-generation.md](../design/02-pulse-generation.md) |

## Why the FET row changed

The BSS138 family (three rows above) was selected under the earlier
resistive-gate-load model, before the crowbar application was identified.
Under that model, BSS138N itself was unorderable (zero stock, 48-week lead
time), so the in-stock Diodes BSS138-7-F was substituted for a first build.
Once the crowbar topology replaced that model, none of the BSS138 variants
were still the right part electrically (see
[../design/03-driver-and-fet.md](../design/03-driver-and-fet.md)), so BSS806N
replaced all three rather than needing its own stock workaround — it was
already in stock. See
[../decisions/decision-log.md](../decisions/decision-log.md) for the full
sequence.
