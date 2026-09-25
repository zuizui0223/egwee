# CFTQ0135 Comarum population-level recovery gate — 2026-09-24

## Frozen target

Programme: `P2_CF01_COMARUM_2014`.

The frozen gradient contract requires, on one common population frame:

- source-defined 500-m population-isolation / woody-area-cover exposure;
- total direct pollinator visitation rate;
- open-pollinated viable seed set.

Independent unit = population/site; maximum n = 14.

## Public-source audit

The open PLOS article makes the exposure and interaction layer unusually transparent.

### Recoverable at population level

Table 1 publishes for each of the 14 populations:

- population identity;
- population surface;
- population closure;
- **population isolation (%)**, defined as woody-area cover within 500 m;
- observation effort;
- bumble-bee abundance and visitation rate;
- solitary-bee abundance and visitation rate;
- other-insect abundance and visitation rate.

Thus the source exposure and an all-visitor I endpoint could be reconstructed without using
within-population plots as independent units.

### Not recoverable under the frozen contract

Open-pollinated seed set is shown by population and year in **Figure 3**. Table 3 reports model
F-statistics for spatial/pollinator predictors but does not expose the required population-level
open-seed-set vector.

No machine-readable supplementary table containing that population-level F vector was identified in
the public article surface used for this audit.

## Decision

Status: **design-valid, quantitatively blocked by population-level F recoverability**.

No EGWEE Fisher-z effect was calculated. This is not an ecological null: the source reports clear
relationships between visitation and seed set, but the available reporting surface does not permit
the registered population-level I-F effect and covariance to be reconstructed without creating data
from a figure.

## No rescue

Do not:

- digitize Figure 3;
- back-calculate population seed set from Table 3 F-statistics;
- substitute supplemental hand-cross seed set for open-pollinated F;
- use population-year rows or 15 observation plots/population as independent fragmentation units;
- select a bee taxon because its source association is stronger;
- replace the frozen 500-m isolation variable with population surface or closure after seeing results.

Reopen only if an authoritative public table/data file or author-provided data exposes
population-level open-pollinated seed set.
