# CFTQ0344 Duckeodendron direct C-F recovery gate — 2026-09-27

## Programme

Programme identity: `P2_CF01_CRAMER_DUCKEODENDRON_2007`.

Primary sources:

- Cramer (2007), LSU doctoral dissertation,
  doi:10.31390/gradschool_dissertations.3052;
- Cramer et al. (2007), *Biotropica*, Duckeodendron seed-dispersal paper,
  doi:10.1111/j.1744-7429.2007.00317.x.

The biological design is unusually attractive for C-F recovery because direct fruit production and
direct seed dispersal were measured around the same focal trees.

## Source common frame

In the 2002 dry season the source selected **11 fruiting Duckeodendron adults**:

- 4 trees in 10-ha fragments;
- 2 trees in 100-ha fragments;
- 5 trees in continuous forest.

The 10-ha and 100-ha trees were combined into a single source-defined fragment class after the source
found no detectable difference in percent dispersal between those fragment sizes.

The same programme was followed through the 2002, 2003 and 2004 fruit crops, with one continuous
tree added in 2003 and one 100-ha tree lost in 2004 after a treefall. Repeated years therefore cannot
be treated as new fragmentation replicates.

The source analysis explicitly includes **tree nested in forest type** as a random effect.

## Locked biological layers

Primary C candidate = direct seed-dispersal support from the focal-tree dispersal transects.

The broad source measures include:

- proportion of seeds dispersed more than 1 m beyond the crown;
- mean dispersal distance;
- distance of the five furthest dispersed seeds.

A direct C-F recovery would have to freeze one C endpoint before calculating standardized effects.

Primary F = directly observed fruit fall / seed crop around the same focal trees.

Fruit fall is a realised reproductive-output quantity and is biologically eligible for
`F_reproductive_function`.

## What the public source actually reports

The public article/thesis provides strong source-model results but not a canonical EGWEE direct
effect table.

For example:

- fruit fall is reported on the log scale as a mixed-model forest-type contrast, with continuous
  forest higher than fragments;
- percent dispersed, dispersal distance and furthest-seed distance are reported through GLMM/MIXED
  tests and source figures;
- Figure 2.3 displays individual-tree dispersal curves graphically rather than as a machine-readable
  common tree table.

The different endpoints use different response distributions and transformations.

The public reporting surface does **not** expose one authoritative table containing the same focal
tree IDs with:

1. a frozen direct C value;
2. fruit-fall F;
3. forest type;
4. reserve/site membership;
5. a dispersion structure permitting canonical Hedges-g marginal variances.

## Why model-test back-conversion is not used

The frozen EGWEE direct stream uses the canonical Hedges-g family and requires compatible marginal
sampling variances at the declared independent-unit level.

Reverse-converting heterogeneous F statistics from negative-binomial, Poisson and transformed mixed
models into standardized mean differences would create a new effect representation after the source
results are visible.

Figure digitization of individual-tree curves or fruit fall is likewise not authorized.

## Reserve nesting

The source confirms that focal trees occur in BDFFP fragments and nearby continuous-forest census
plots, but the public effect reporting does not expose an exact tree-to-reserve table suitable for
reconstructing higher-level forest/reserve dependence.

This does not invalidate the source study. It means EGWEE cannot certify an independent-unit
sampling variance for the direct C-F meta-analytic family from the current public reporting surface.

## Terminal decision

`blocked_Duckeodendron_common_tree_CF_marginals_and_forest_nesting_not_recoverable`

Direct C-F programme increment: **0**.

Duckeodendron is retained as a strong **process-function fragmentation anchor**:

- fruit fall is lower in fragments;
- seed dispersal quantity and quality are lower in fragments;
- fragmentation effects on dispersal are strongest in high-fruit years.

Those source-supported directions are ecologically useful, but they are not promoted to a new direct
C-F programme without effect-unit-valid marginal variances.

## Bocageopsis boundary

*Bocageopsis multiflora* is a dependent comparison panel inside the same dissertation/programme.
It cannot become a second independent C-F programme.

Its fruit-production and dispersal sampling frames also differ from Duckeodendron, so it cannot be
used to patch a missing Duckeodendron marginal effect.

## Reopening condition

Reopen only if an authoritative source supplies either:

- focal-tree C and F values plus forest/reserve membership for the common campaign frame; or
- a source-model standardized contrast and sampling variance that can be shown to belong to the
  frozen EGWEE direct effect family without post-result conversion.

## No rescue

Do not:

- treat repeated tree-years as independent fragmentation units;
- treat seeds, distances or transects as fragmentation n;
- reverse-engineer Hedges g from endpoint-specific F statistics after outcome inspection;
- digitize individual-tree figures to manufacture the common C/F table;
- ignore forest/reserve nesting because tree-level replication is convenient;
- select whichever C endpoint gives the strongest C-F separation;
- count Bocageopsis as a second independent programme;
- use the programme to validate a finite EGWE/NEE operator.
