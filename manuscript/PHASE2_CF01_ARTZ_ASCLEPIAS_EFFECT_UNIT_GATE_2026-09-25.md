# CFTQ0235 Artz–Waddington Asclepias repeated-island I-F gate — 2026-09-25

## Candidate

Programme identity: `P2_CF01_ARTZ_ASCLEPIAS_2006`.

Primary source: Artz & Waddington (2006), *Journal of Ecology* 94:597–608,
doi:10.1111/j.1365-2745.2006.01109.x.

The source uses **11 bayhead tree islands** in the Everglades:

- 5 small islands (5–10 m²);
- 6 large islands (20–30 m²).

The same islands anchor permanent marl-prairie sampling positions at approximately:

- 25 m;
- 100 m;
- 300 m;
- 700–1000 m.

Pairs of potted *Asclepias lanceolata* plants were placed at those positions and direct insect visits,
fruit production and seed production were measured.

## Biological eligibility

The biology is an excellent I-F landscape-isolation test:

- pollinator activity declines with distance from tree islands;
- fruit and seed production decline with distance;
- island size is a prespecified source attribute;
- I and F arise from the same experimental landscape architecture.

## Effect-unit problem

The highest independent landscape unit is **tree island (n=11)**.

The public source does not expose one common island-level I/F vector:

- visitation observations are explicitly **pooled by distance class** within small- and large-island
  categories;
- reproductive analyses retain repeated distance-site observations nested within the same islands;
- seed-production regressions report approximately `n=40` for small-island sampling positions and
  `n=48` for large-island sampling positions.

Those 40/48 observations are not 40/48 independent landscapes. They are repeated positions around
5 or 6 source islands.

The publication therefore does not support a simple Fisher-z calculation using 40/48 as n, and the
pooled I reporting prevents retrospective reduction to 11 paired island-level I/F values.

## Decision

Status:
`blocked_repeated_island_IF_effect_unit_not_recoverable`.

No I-F effect is admitted. This is an **effect-unit/reporting limitation, not an ecological null**.

## Reopening condition

Reopen only if authoritative raw/author-provided data expose island identity for both:

- direct *Asclepias* visitation;
- fruit/seed production;

at the repeated distance positions.

A future recovery must then freeze one of the following before outcomes are recomputed:

1. a repeated-measures/hierarchical distance model with tree island as the clustering unit; or
2. one predeclared island-specific distance-response parameter per layer, followed by an
   island-level comparison.

## No rescue

Do not:

- treat island × distance positions as independent landscape replicates;
- use `n=40` or `n=48` as fragmentation n;
- mix pooled distance-class I with individual distance-site F as if they shared one sampling frame;
- choose small versus large islands after seeing which stratum is stronger;
- digitize figures to invent island-specific vectors;
- interpret the source's strong ecological pattern as validation of a finite EGWE/NEE operator.

All terminal outcomes are retained.
