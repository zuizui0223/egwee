# SF05-71 / Heliconia acuminata Phase-2 recovery contract

**Locked:** 2026-09-19 before quantitative Heliconia effects are committed to EGWEE.

## Discovery-stage disclosure

The full source article and its tables are publicly readable and were inspected before this recovery contract was written. This is therefore not labelled an outcome-blind preregistration.

To constrain analytical flexibility, endpoint identity, exposure, independent unit, orientation and covariance method are fixed below from the existing EGWEE layer definitions and source measurement roles. They are not selected by the sign or statistical significance of the resulting fragmentation contrasts.

## Goal

Test whether Côrtes et al. 2013 can contribute a same-system Phase-2 multilayer fragmentation cluster from five independent Heliconia acuminata sites in the BDFFP experimental landscape.

## Fragmentation exposure and independent unit

Primary independent unit = **site/plot**.

The fixed source-defined binary exposure is:

- fragmented: F1, F2, F3 — three 1-ha forest fragments;
- reference: CF1, CF2 — two continuous-forest sites.

Flowering plants, reproductive plants, seedlings, microsatellite loci and individual parentage events are nested observations and do not increase fragmentation-level n.

Plant density is retained as a biological covariate/moderator candidate only. It does not replace the source fragmentation contrast in this direct Hedges-g recovery.

## Locked primary layers and endpoints

### C — movement/connectivity

Primary C endpoint = **percentage of seedlings whose father is outside the 1.26-ha sampled plot** from source Table 2.

This is fixed because it is a direct pollen-immigration quantity on all five sites and maps directly onto the EGWEE movement/connectivity layer.

Do not switch after effect inspection to parent-pair-outside percentage, mother-outside percentage, modal pollen distance, modal seed distance, reproductive dominance or plant density.

Orientation multiplier = `+1`: larger father-outside percentage means greater pollen connectivity support.

### G_adult

Primary G_adult endpoint = **unbiased expected heterozygosity (UHe) of reproductive plants** from source Table 3.

Orientation multiplier = `+1`.

### G_offspring

Primary G_offspring endpoint = **unbiased expected heterozygosity (UHe) of seedlings** from source Table 3.

Orientation multiplier = `+1`.

The adult and offspring metrics are deliberately matched on the same UHe scale and the same five-site exposure frame.

## Effect calculation

For each endpoint use the canonical direct EGWEE Hedges-g estimator:

- `d = (M_frag - M_ref) / s_p`;
- `df = n_frag + n_ref - 2`;
- `J = 1 - 3/(4df - 1)`;
- `g = J d`;
- `V(g) = 1/n_frag + 1/n_ref + g^2/[2(n_frag+n_ref)]`.

Here `n_frag = 3` and `n_ref = 2`, corresponding only to independent sites.

## Within-cluster dependence

The three endpoint effects share the same five sites. Follow the pre-existing paired-unit covariance hierarchy:

1. fit an intercept plus the fixed fragmented/reference indicator separately to the five site-level values for C, G_adult and G_offspring;
2. retain the three residual vectors;
3. calculate their residual-correlation matrix R;
4. construct `V_ij = R_ij * sqrt(v_i*v_j)` using the canonical marginal variances;
5. require the full 3x3 working covariance matrix to be positive definite before admitting a joint three-layer cluster.

If the full matrix is not positive definite, no numerical ridge is added solely to force admission. Pair-specific positive-definite blocks may still be retained under the Phase-2 pair rules.

## No-rescue rules

Do not:

- change the fragment/reference labels after viewing effects;
- treat plants, seedlings, loci or parentage assignments as independent sites;
- replace father-outside percentage with another dispersal metric because its effect is stronger;
- replace UHe with Na, Fis or sp after viewing direction;
- use density instead of fragmentation because it explains more variation in the source study;
- set within-cluster covariance to zero;
- count C, G_adult and G_offspring as separate independent programmes.

Possible terminal states include:

- `P2_SF05_71_admitted_C_Gadult_Goffspring_covariance_aware`;
- `P2_SF05_71_pair_specific_only`;
- `P2_SF05_71_covariance_not_positive_definite`;
- `P2_SF05_71_source_values_not_reconstructable`.

All terminal outcomes are acceptable.
