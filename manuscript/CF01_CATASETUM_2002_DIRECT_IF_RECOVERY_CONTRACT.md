# CFTQ0278 / Catasetum viridiflavum direct I-F recovery contract — 2026-09-25

## Programme

Programme identity: `P2_CF01_CATASETUM_2002`.

Primary source: Murren (2002), *Journal of Ecology* 90:100–107,
doi:10.1046/j.0022-0477.2001.00638.x.

This is a **retrospective external recovery**. The source's year-specific directions are published.
The common-year/common-site rule below is therefore fixed to prevent choosing the year with the
largest island–mainland difference.

## Source geometry

The full study follows:

- 10 Panama Canal island sites (forest fragments);
- 5 mainland large-forest sites;
- three years of reproductive observations.

However, the replicated direct pollinator-abundance survey was conducted in **1997** on:

- five island sites;
- five mainland sites.

EGWEE therefore restricts the direct I-F candidate to the exact **1997 ten-site overlap**.

## Independent unit

Independent unit = **site/population**.

Baiting days, individual bees, orchid plants, flowers, pollinia and fruiting events are nested below
site and never increase fragmentation n.

## Locked contrast

Fragmented = island forest site.

Reference = mainland continuous/large-forest site.

No island-size threshold or alternative year is selected.

## Locked I endpoint

Primary I = **1997 site-level abundance of Eulaema cingulata**, the sole pollinator, measured as
bees trapped per day under the source's standardized baiting survey.

Pollinarium removal is male reproductive success and is not substituted for I.

## Locked F endpoint

Primary F = **1997 female reproductive success measured as fruit set** on the same ten-site frame.

Fruit set from 1996 and 1998 remains temporal context/sensitivity only because direct replicated
pollinator abundance is not measured on the same source frame in those years.

## Marginal effects

If the ten paired site values are recovered:

1. calculate Hedges `g` for island minus mainland for I;
2. calculate Hedges `g` for island minus mainland for F;
3. use the canonical EGWEE large-sample SMD variance;
4. orient negative values as lower biological support/function on islands.

No lower-level plant or bait-day count may enter `n`.

## I-F dependence

If the same ten site identities provide I and F:

1. group-center I and F within island/mainland condition;
2. calculate the site-level residual/outcome correlation proxy `rho_IF`;
3. construct `Cov(g_I,g_F) = rho_IF * sqrt(V_I * V_F)`;
4. require positive-definite 2x2 covariance and positive `Var(g_I-g_F)`.

If valid marginal effects are recoverable but paired covariance cannot be reconstructed, preserve
one programme cluster and use the frozen cluster-robust fallback; never set covariance to zero by
convenience.

## Admission

Admit at most one direct I-F programme if:

- the exact 1997 five-island + five-mainland site identities are recoverable;
- site-level bee abundance is recoverable;
- site-level 1997 fruit set is recoverable;
- marginal sampling variances correspond to sites;
- the common frame is not enlarged with other years.

## No rescue

Do not:

- choose 1996 or 1998 because fruit-set differences were stronger;
- use all 15 reproductive sites while I uses only ten sites;
- count baiting days, bees, plants or flowers as fragmentation replicates;
- use pollinarium removal as a replacement I endpoint;
- treat three years as three independent programmes;
- count islands separately as programmes;
- call 1997 nonsignificance equivalence;
- use the result to validate an EGWE/NEE finite operator.

## Terminal outcomes

- `catasetum_1997_direct_IF_covariance_aware`;
- `catasetum_1997_direct_IF_cluster_robust`;
- `catasetum_1997_site_identity_not_recoverable`;
- `catasetum_1997_site_level_I_not_recoverable`;
- `catasetum_1997_site_level_F_not_recoverable`;
- `catasetum_1997_marginal_variance_not_effect_unit_valid`.

All outcomes are retained.
