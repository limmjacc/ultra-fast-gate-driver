# Data reliability

This project draws on two different kinds of source, and they are not
equally trustworthy. This note exists so that distinction stays visible
rather than getting flattened once a number lands in a table.

## Read directly from a datasheet PDF

Every electrical figure in
[datasheet-notes.md](datasheet-notes.md) and in
[../design/](../design/README.md) that is attributed to a specific part was
read from the actual manufacturer PDF, saved in `hardware/datasheets/`, not
from a search summary. These are as reliable as the datasheet itself (subject
to the normal caveats: typical vs. maximum figures, test conditions that may
not match this circuit, and revision currency — each checked and noted where
it matters, for example BSS806N's switching-time figures being measured
under conditions this circuit does not use).

## Derived in this project (marked **Estimate**)

Anything computed from datasheet figures — the COSS de-rating in
[../design/04-timing-and-recovery.md](../design/04-timing-and-recovery.md),
the drain-edge and recovery-time tables, the LED resistor value — is marked
**Estimate** wherever it appears. These are first-order, often single-pole,
lumped-element calculations with stated assumptions. Treat them as planning
figures to validate by simulation and measurement, not as specifications.

## Web search and page-fetch summaries

Distributor stock/pricing figures and a few datasheet figures that could not
be retrieved directly (for example the Würth LED's forward voltage) came from
either a search engine's generated summary of multiple pages, or a page-fetch
tool that returns a *model-generated summary* of a page rather than its
verbatim text (digikey.ca in particular blocks direct automated requests,
requiring this approach). Two concrete reasons this matters:

- **Search-snippet and page-fetch figures disagreed with each other more
  than once in this project.** For example, early search snippets showed
  LMG1025QDEERQ1 at 2,584 units in stock and LMG1020YFFR at 9,910; a later
  page-fetch read of the same products showed 883 and 0 respectively. Neither
  figure is verifiably more current than the other from this side.
- **A page-fetch summary can misattribute a figure to the wrong product** on
  a page that lists substitutes or cross-references alongside the part
  actually being queried; this happened at least once during sourcing checks
  in this project (see the caveats in [sourcing.md](sourcing.md)).

**Every stock figure, price, and any other figure sourced this way is marked
as such where it appears, and should be re-confirmed in a browser before
being acted on** — particularly before ordering parts or committing a board
layout to a specific footprint.
