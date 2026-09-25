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
