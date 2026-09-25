# Phase-2 SF05-32 Castanopsis quantitative gate — 2026-09-19

## Decision

Wang, Compton & Chen 2011 (*Castanopsis sclerophylla*) is **closed for quantitative Phase-2 admission under the current EGWEE effect streams**.

This is a design/effect-unit closure, not an outcome-based rejection.

## Source design recovered

The source defines three independent study sites with different fragmentation levels:

- HY, Heyang Island — strongly fragmented, 13 ha;
- LS, Laoshan Island — moderately fragmented, 875 ha;
- XS, Xianshan Peninsula — continuous-forest control, >2500 ha.

One 130 m × 130 m plot was sampled at each site. Trees were divided into prefragmentation (>50 years) and postfragmentation (<50 years) cohorts using basal diameter as an age proxy. The three sites therefore produce six cohort subpopulations, but the **fragmentation-level independent unit remains the site**, not the cohort or tree.

The public Dryad archive remains useful for reproducibility and mechanistic analyses, but individual-level raw data cannot create additional independent fragmentation units.

## Why the primary direct stream cannot open

A direct binary Hedges-g contrast would have:

- fragmented: HY + LS = 2 independent sites;
- reference: XS = 1 independent site.

The reference group therefore has no fragmentation-unit sampling SD. Nested pre/post cohorts cannot be re-labelled as independent reference/treatment replicates.

## Why the gradient stream cannot rescue it

Treating HY → LS → XS as a three-site fragmentation-severity gradient would give n=3 independent sites.

The canonical EGWEE Fisher-z sampling variance is `1/(n-3)`, which is undefined at n=3. The gradient stream therefore also fails its quantitative effect-unit requirement.

## Biological information retained

The source remains informative mechanistically because it measures adult-history versus postfragmentation cohorts, genetic diversity, selfing, fine-scale SGS and dispersal-related quantities across a controlled fragmentation series.

Those observations can be cited as mechanistic/contextual evidence, but they do not increment any pair-specific Phase-2 programme count.

## Terminal status

`P2_SF05_32_closed_insufficient_fragmentation_unit_replication`

No Castanopsis effect size is added to the Phase-2 synthesis.
