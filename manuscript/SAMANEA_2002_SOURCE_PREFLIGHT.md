# ML016 / PS021 Samanea saman source preflight

## Status

`candidate_under_recovery`; **not admitted**.

This note records source facts available before table-level effect extraction.

## Verified source-level facts

- Species: *Samanea saman*.
- Region: tropical dry forest, Costa Rica.
- Source-defined exposure is a direct two-group fragmentation contrast:
  - isolated trees >500 m from nearest conspecific in agricultural/pasture/small-remnant matrix;
  - continuous-population trees at >=10 conspecifics/ha in undisturbed forest.
- The paper reports biological responses spanning pollination/reproductive performance, progeny mating/genetic state, and progeny vigour.
- Independent biological replication is by maternal tree; flowers, fruits, seeds, progeny and loci are nested.

## Sampling-frame warning

Secondary source summaries indicate that different analyses use different maternal-tree subsets:

- genetic diversity/selfing: 17 isolated vs 20 continuous trees;
- reproductive/pollination traits: 27 isolated vs 24 continuous trees;
- greenhouse progeny-vigour experiment: 10 isolated vs 14 continuous maternal trees.

Therefore ML016 cannot be treated as a paired same-row multivariate cluster by default. Admission requires the primary article to establish enough overlap or a defensible dependence representation for at least two retained layer effects. Large seed/flower counts cannot substitute for maternal-tree replication.

## Directional information already public

The abstract/review literature already reveals qualitative directions (for example greater progeny selfing/inbreeding and lower progeny vigour under isolation). This candidate is therefore **not outcome-blind at the qualitative discovery stage**. The locked contract only protects against table-level numeric endpoint/p-value shopping. Any eventual manuscript language must preserve that distinction.

## Next gate

Open the primary article tables/methods and recover, for each prospectively eligible layer:

1. exact maternal-tree n by condition;
2. mean/SD or other sufficient statistics at maternal-tree level;
3. whether the same maternal trees underlie multiple endpoints;
4. covariance-relevant paired/tree-level information if available.

If at least two layers cannot be placed in `hedges_g_direct` without pseudo-replication and with defensible within-cluster dependence, close ML016 as `effect_unit_or_covariance_not_reconstructable` rather than changing the effect family.
