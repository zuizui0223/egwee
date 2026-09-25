# CFTQ0301 Spondias mombin C-F effect-unit gate — 2026-09-25

## Programme

Programme identity: `P2_CF01_SPONDIAS_MOMBIN_1997`.

Primary source: Nason, Aldrich & Hamrick (1997), *Journal of Heredity*,
doi:10.1093/oxfordjournals.jhered.a023104.

The article contains original empirical case studies of gene flow and reproductive consequences of
forest fragmentation. The *Spondias mombin* case is the relevant C-F candidate.

## Biological signal already visible

The source reports two contrasting responses in the *Spondias* fragment system:

- fruit production / germination are reduced in small fragments;
- progeny in small fragments show approximately **90–100% pollen immigration**, with inferred pollen
  sources roughly **80–1000 m** away.

This is an ecologically important candidate for movement/connectivity persistence alongside reduced
reproductive function.

Because those directions are already public, the recovery is explicitly retrospective.

## Frozen contrast

Primary fragmented condition = **small island fragments**.

Primary reference condition = the source continuous-forest populations **FDP + LC**.

The larger island/fragment **DL** remains source context / sensitivity and is not inserted into the
primary contrast after seeing outcomes.

The five *Ficus* species discussed in the same article are separate pollen-flow case studies. They
are C-only context and **do not increase C-F programme K**.

## Locked layers

Primary C = population-level pollen immigration / interfragment gene-flow support from the
*Spondias* progeny/paternity analysis.

Primary F = population-level fruit production / fecundity.

Germination is secondary and cannot replace fruit production because it is easier to reconstruct or
has a stronger response.

## Effect-unit problem

C is reported at a population / fragment level.

Fruit production is shown largely as individual-tree fruit output against DBH in the published
figure. Individual trees are nested within population/fragment and cannot become fragmentation
replicates.

No direct Hedges-g C-F effect is calculated unless an authoritative source permits fruit production
to be aggregated to the same population units used for C with a defensible marginal sampling
variance.

Figure digitization of individual trees is not authorized by this gate.

## Dependence

If valid population-level C and F marginals are recovered on the same contrast but paired covariance
is unavailable, preserve one programme cluster and use the already-frozen cluster-robust fallback.
Do not set covariance to zero.

## Terminal outcomes

- `spondias_mombin_direct_CF_covariance_aware`;
- `spondias_mombin_direct_CF_cluster_robust`;
- `spondias_mombin_population_F_not_recoverable`;
- `spondias_mombin_common_population_CF_frame_not_recoverable`;
- `spondias_mombin_marginal_variance_not_effect_unit_valid`.

## No rescue

Do not:

- use individual trees as population/fragment n;
- digitize the fruit-production figure to invent a population variance;
- select germination instead of fruit production after seeing results;
- combine DL with the small islands because it improves a contrast;
- count the five *Ficus* species as extra C-F programmes;
- interpret high pollen immigration as proof that fragmentation has no biological effect;
- use this result to validate a finite EGWE/NEE operator.

All terminal outcomes are retained.
