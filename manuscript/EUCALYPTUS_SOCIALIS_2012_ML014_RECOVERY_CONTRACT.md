# ML014 / Eucalyptus socialis 2012 cluster-recovery contract

**Locked:** 2026-09-13, before public Dryad family-level numeric outcome rows are opened.

## Goal

Test whether Breed et al. (2012), *Molecular Ecology* 21:5955–5968, DOI `10.1111/mec.12056`, can contribute a fourth independent primary multilayer fragmentation cluster without using the cross-landscape Yookamurra comparison or lower-level progeny as fragmentation replication.

The source sampled mother trees from three landscape contexts. The primary EGWEE contrast is restricted to the two **Monarto** contexts because the paper explicitly treats the within-Monarto comparison as the cleaner same-landscape test:

- reference: Monarto small remnant woodlands;
- fragmented: Monarto isolated pasture trees.

Yookamurra large intact woodland is retained as source context/sensitivity only and is not pooled into the primary contrast.

## Independent-unit frame

Primary independent unit = maternal tree / progeny family.

Source counts before any Dryad numeric outcome access are:

- Monarto small remnant woodland: 16 mother trees;
- Monarto isolated pasture: 13 mother trees.

Seedlings, microsatellite loci, repeated growth observations and individual progeny remain nested below family and cannot become fragmentation replicates.

If either primary layer is available only at group level rather than family level, terminate rather than pairing group dispersion with family `n`.

## Locked exposure

Binary source-defined Monarto landscape context:

- `reference = small_remnant_woodland`;
- `fragmented = isolated_pasture`.

No post-outcome replacement with continuous density, Yookamurra-vs-Monarto, geographic distance, inbreeding class or another ecological predictor is allowed.

## Locked primary G_mating layer

Primary mating-support endpoint = **family-level multilocus correlated paternity `r_p`**, oriented as biological support by multiplying the Hedges-g effect by `-1`.

Rationale fixed before opening Dryad numeric rows:

- the source analyses family-level mating parameters;
- in the paper's all-family fitness model comparison, `growth ~ r_p` is the top-ranked pollen-diversity model and explains the most deviance (16.6%);
- higher `r_p` means fewer effective pollen donors / lower pollen diversity;
- therefore lower `r_p` represents greater mating/pollen-diversity support.

Do **not** switch after value access to `k_n`, `t_m`, `t_m-t_s`, `r_s`, `r_o`, adult/progeny heterozygosity, or an inverse transformation such as `1/r_p` merely because it produces a stronger contrast. Those are context/sensitivity representations, not additional primary layers.

If the public family-level data do not expose the source-consistent family `r_p` representation, terminate `family_level_rp_not_reconstructable`.

## Locked F layer

Primary reproductive/offspring-function endpoint = **family-level mean progeny growth (height)** from the common-garden experiment.

Preferred source representation is a family-level growth field in `MECBreedfamily.csv`. If growth is available only as individual progeny rows in `MECBreedprogeny.csv`, aggregate offspring to one arithmetic mean per maternal family before any landscape contrast is calculated.

The family, not the seedling, remains the independent unit.

Do not switch after value access to germination, survival, heterozygosity, inbreeding load, another time point or another fitness response because it is more favourable.

If family-level mean growth cannot be reconstructed on the same maternal-family identifiers used by `r_p`, terminate `family_level_growth_not_reconstructable`.

## Common-frame rule

Primary C/G_mating–F admission uses the exact intersection of Monarto maternal families with both:

1. source-consistent family `r_p`;
2. family mean growth.

Both Hedges-g effects and the dependence proxy are calculated on that same complete-case family frame. No family is removed based on effect direction.

Require at least two independent families in each Monarto landscape context after the common-frame intersection. The source design is expected to contain substantially more, but missing public rows are not back-filled.

## Effect representation

For each locked endpoint on the common family frame:

- calculate fragmented-minus-reference Hedges g;
- use the repository canonical `metafor::escalc(measure="SMD", vtype="LS")` sampling-variance convention:

`V(g) = 1/n_fragmented + 1/n_reference + g^2 / [2(n_fragmented+n_reference)]`;

- F growth is oriented directly: negative = lower growth under isolated pasture fragmentation;
- raw `r_p` g is stored, then `orientation_multiplier=-1` so negative oriented G_mating effect = lower pollen-diversity support under fragmentation.

Family counts, not progeny counts or loci, enter the fragmentation-level variance.

## Within-cluster dependence

The two effects share the same maternal-family rows and are not independent.

After both family vectors are recovered:

1. orient the family-level mating-support vector as `-r_p`;
2. group-center mating support and growth within the two Monarto contexts;
3. calculate their Pearson residual/outcome correlation proxy `rho`;
4. construct the working 2x2 sampling covariance as `Cov_GF = rho * sqrt(V_G * V_F)`;
5. require finite positive marginal variances and a positive-definite 2x2 covariance matrix.

If dependence cannot be reconstructed, do not set covariance to zero and do not add a ridge. Terminate `dependence_not_reconstructable` for covariance-aware admission; any valid marginal effects may remain descriptive/sensitivity evidence.

## Source-opening order

1. lock this contract;
2. inspect Dryad metadata and CSV headers/schema only;
3. verify that landscape-context and maternal-family identifiers can link the family-level mating and growth records;
4. if the family `r_p` and growth fields are structurally present, freeze any exact column-name/aggregation mapping needed without printing numeric outcome rows;
5. only then open the numeric rows once and calculate the two effects and covariance;
6. retain concordant, discordant, null, imprecise or non-identifiable outcomes without rescue.

## No-rescue rules

Do not:

- include Yookamurra in the primary Monarto contrast;
- use seedling count, locus count or repeated observations as fragmentation `n`;
- choose `k_n` instead of `r_p` after seeing values;
- replace growth with another fitness endpoint after seeing values;
- use group Table 1 means/SDs with maternal-family `n` if family-level values are unavailable;
- change the exposure from Monarto landscape context to continuous density after outcome access;
- drop complete-case families because they weaken an effect;
- set within-cluster covariance to zero;
- count G_mating and F as two independent studies.

## Possible terminal states

- `ML014_admitted_Gmating_F_covariance_aware`;
- `family_level_rp_not_reconstructable`;
- `family_level_growth_not_reconstructable`;
- `common_family_frame_insufficient`;
- `dependence_not_reconstructable`;
- `source_access_blocked`.

All terminal outcomes are acceptable.
