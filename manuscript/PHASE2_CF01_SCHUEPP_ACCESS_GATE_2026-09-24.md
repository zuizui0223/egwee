# CFTQ0156 Schüepp cherry common-site recovery gate — 2026-09-24

## Frozen target

Programme: `P2_CF01_SCHUEPP_CHERRY_2014`.

The frozen retrospective gradient contract requires a common site-level frame containing:

- woody-habitat isolation = distance to the nearest woody habitat;
- all-potential-pollinator cherry visitation rate;
- open/control fruit set.

Independent unit = landscape sector / experimental site; maximum source n = 30.

## Public-source audit

The open article and public thesis/repository surfaces reproduce the experimental design:

- 30 spatially separated landscape sectors;
- seven standardized cherry trees per site;
- source exclusion of two sites from fruit-set analysis;
- source exclusion of three sites from visitation analysis;
- woody-habitat amount and isolation measured independently;
- cherry isolation and cherry amount measured separately.

The available supporting material exposes:

- visitor-group totals / scoring information;
- explanatory-variable definitions;
- a correlation matrix among landscape/local explanatory variables;
- fitted model summaries and response figures.

It does **not** expose one authoritative table or machine-readable vector that joins, by site ID:

1. woody-habitat isolation;
2. all-potential-pollinator visitation;
3. open/control fruit set.

The exact I-F common site intersection therefore cannot be reconstructed without reading response
values from figures or reverse-engineering fitted models.

## Decision

Status: **design-valid, quantitatively blocked by common-site I/F vector recoverability**.

No EGWEE Fisher-z effect was calculated.

This is not an ecological null. The source itself reports landscape and pollination relationships;
the stop concerns the independent-unit data surface needed for the registered covariance-aware
cross-layer effect.

Gradient programme increment: **0** at this gate.

## No rescue

Do not:

- digitize response figures;
- back-calculate site values from GLM/GLMM coefficients or deviance tables;
- use published fitted coefficients as if they were site-level Pearson correlations;
- replace woody-habitat isolation with cherry isolation or woody-habitat amount because those
  relationships are better reported;
- use seven trees/site, flowers, visits or fruits as landscape n;
- choose different site subsets for I and F.

Reopen only if an authoritative public or author-provided source exposes the common site-level
woody-isolation, visitation and open-fruit-set vectors.
