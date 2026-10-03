# CFTQ0267 Quesada bombacaceous I-F effect-unit gate — 2026-09-25

## Candidate

Programme identity: `P2_CF01_QUESADA_BOMBACACEOUS_2004`.

Primary source: Quesada et al. (2004), *Biotropica* 36:131–138.
The source is indexed under legacy DOI `10.1646/q1571` and Wiley DOI
`10.1111/j.1744-7429.2004.tb00305.x`.

The paper directly evaluates forest-fragmentation effects on bat visitation and reproductive success
in three bombacaceous tree species:

- *Ceiba aesculifolia*;
- *Ceiba grandiflora*;
- *Ceiba pentandra*.

## Programme identity

The three species are **dependent panels inside one publication programme**, not three independent
cross-system programmes.

Their geography and response availability differ:

- *C. aesculifolia* and *C. grandiflora* are explicit forest-versus-fragment I/F candidates;
- *C. pentandra* is sampled across Chamela plus Costa Rican contexts and its direct F eligibility
  must be verified rather than assumed.

## Effect-unit issue

The source reports pollinator activity per filmed flower/inflorescence, while reproductive success is
measured on trees. Published reproductive sample sizes include tree-level forest/fragment groups,
whereas the pollinator table reports filmed flowers/inflorescences.

Therefore flower/inflorescence counts cannot automatically become the independent fragmentation n
for I.

Before any direct Hedges-g effect is calculated, each species panel must establish:

1. the source forest/fragment habitat contrast;
2. the independent tree/local-context units contributing to I;
3. the independent tree units contributing to F;
4. whether those frames are shared, nested or only partially overlapping;
5. marginal sampling variance at the legitimate independent-unit level.

## Companion-paper audit

The linked species-specific companion paper is Quesada et al. (2003), *Oecologia* 135:400–406,
doi:10.1007/s00442-003-1234-3, for *Ceiba grandiflora*.

It does not remove the effect-unit problem.

- visitation was recorded from **35 flowers on 15 disturbed trees** and **43 flowers on 24
  undisturbed trees**, with 1–3 flowers per tree and repeated recording nights;
- the visitation model uses the number of visits per flower/night and publishes model/LS-mean
  summaries rather than one tree-level visitation value and variance per independent tree/context;
- fruit set is directly measured per tree on **17 disturbed and 18 undisturbed trees**.

Thus the F marginal is tree-level, but the public I marginal remains a nested flower/night
representation. The 2004 multispecies paper uses the same kind of filmed-flower/inflorescence
reporting for visitation.

The companion paper therefore cannot be used to attach tree n to flower-level I dispersion.

## Decision

Status: `close_tree_level_I_marginal_variance_not_reconstructable`.

No Ceiba species panel currently has a publicly reconstructable direct I marginal effect whose
sampling variance corresponds to the required tree/local-context independent unit.

The cluster-robust fallback remains relevant only **after valid marginal I and F effects exist**. It
solves unknown within-cluster covariance; it cannot repair a marginal effect whose variance is
defined on the wrong observation level.

Direct I-F programme increment: **0**.

The ecological mechanism is retained: forest disruption is associated with lower effective bat
visitation/pollen receipt and lower fruit set in *C. grandiflora*. That biological result is not
promoted into the primary Hedges-g I-F family without the effect-unit-valid I marginal.

## Reopening condition

Reopen only if an authoritative source or author-provided data supplies tree-level visitation
summaries/raw observations with tree identity sufficient to estimate the forest-versus-disturbed I
marginal at the same legitimate tree/local-context level as F.

## Dependence rule

If valid marginal I and F effects share the same species/habitat contrast but paired covariance is
not reconstructable, retain the effects in **one cluster** and use the already-frozen cluster-robust
fallback. Do not set covariance to zero.

This fallback cannot rescue invalid marginal variances.

## Endpoint rule

Primary I candidate = total bat visitation rate per flower/inflorescence, reconstructed to the
legitimate tree/local-context effect unit.

Primary F candidate = fruit set.

Flower production is D/resource support and cannot replace F merely because it is better reported.

Mating-system quantities remain separate C/G_offspring context unless they satisfy another frozen
pair contract.

## Admission

At most **one direct I-F programme increment** can come from this publication programme regardless
of how many Ceiba species are eligible.

Species-specific panels remain visible inside the cluster. They cannot be counted as independent K.

## Terminal outcomes

- `quesada_bombacaceous_direct_IF_cluster_robust`;
- `quesada_species_tree_level_I_not_reconstructable`;
- `quesada_species_common_IF_frame_not_reconstructable`;
- `quesada_marginal_variance_not_effect_unit_valid`;
- `quesada_no_species_with_common_direct_IF_frame`.

## No rescue

Do not:

- use filmed flower/inflorescence counts as independent tree n without source support;
- count the three species as three programmes;
- select only the species with the clearest fragmentation effect;
- replace fruit set by flower production;
- import *Pachira quinata* or later *Ceiba* campaigns as if they were synchronous 2004 observations;
- set unknown I-F covariance to zero.

All terminal outcomes are retained.
