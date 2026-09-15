# ML020 / PS022 Aizen–Feinsinger 1994 replicated Chaco cluster-recovery contract

## Goal

Test the fifth independent same-effect-family primary cluster using the replicated Chaco Serrano fragmentation programme of Aizen & Feinsinger (1994). The confirmatory target remains whether the primary state-separation conclusion survives omission of `ML001 Serapias`; a smaller full-corpus p-value is not an admission criterion.

## Discovery-status limitation

The source Appendix I was publicly visible during candidate recovery, so ML020 is **not** claimed to be outcome-blind at discovery. To prevent within-paper species/endpoint selection after seeing those tables, this contract retains **all source-explicit fully replicated species** and one common predeclared endpoint pair rather than selecting the strongest species.

## Source

Aizen MA, Feinsinger P. 1994. Forest Fragmentation, Pollination, and Plant Reproduction in a Chaco Dry Forest, Argentina. Ecology 75:330–351. DOI 10.2307/1939538.

The source states that three habitat treatments were replicated across four study sites for exactly three species: *Prosopis nigra*, *Cercidium australe*, and *Atamisquea emarginata*.

## Independent exposure unit

The independent fragmentation unit is the **site-specific habitat unit**, not the individual plant, flower, fruit, seed, or pollen tube.

Primary direct contrast:

- fragmented = source-defined small fragment (<1 ha);
- reference = continuous forest;
- large fragments remain source context/sensitivity and do not enter the primary two-group Hedges-g contrast.

The four study-site IDs are `1, 2, 3, 5`. For each retained species and endpoint, one habitat-unit mean per site per condition is the observation used for the marginal Hedges g. The source-reported within-habitat individual `n` and SD are provenance only and are not promoted to fragmentation replication.

## Species rule

Retain all three species explicitly identified by the source as having all three habitat treatments replicated across four sites:

1. *Atamisquea emarginata* — single reported sampling season;
2. *Cercidium australe* — use 1990, the repeated-year record on the four-site frame;
3. *Prosopis nigra* — use 1990, because the source explicitly expanded the 1990 sample to the fourth site whereas 1989 lacks the complete four-site frame.

The three species are dependent outcomes inside **one ML020 programme cluster**. They never count as three independent primary clusters.

## Endpoint rule

Use the same pair for every retained species:

- `I_pollen_tubes`: mean number of pollen tubes per flower/style (`PT`), mapped to `I_interaction`;
- `F_fruit_set`: fruit/flower ratio, or fruits per inflorescence for Mimosoideae (`FS`), mapped to `F_reproductive_function`.

Do not substitute pollen grains, seed set, seed output, visit frequency, residual pollen-quality metrics, or a different year because it yields a stronger state-separation contrast.

The source reports that, except for explicitly noted herbaceous species, pollen-tube, fruit-set and seed-set data came from the same sampled individuals. The retained three species are woody/shrub taxa, so PT and FS share the source habitat-unit sampling frame.

## Effect-size contract

For each species and endpoint:

1. form the four continuous-forest habitat-unit means and four small-fragment habitat-unit means;
2. calculate Hedges g for `small - continuous` using those habitat-unit means as `n=4` and `n=4`;
3. use the same Hedges-g / large-sample variance semantics as the existing direct primary stream;
4. orient negative values as reduced biological support/function under fragmentation.

Do not use the source's lower-level individual sample sizes when calculating the primary Hedges-g variance.

## Within-species dependence

PT and FS share study-site habitat units. Reconstruct a covariance proxy separately for each species from the four continuous and four small habitat units:

- group-center PT and FS within condition;
- calculate the Pearson correlation across the eight group-centered habitat-unit observations;
- set `cov(g_I,g_F) = rho * sqrt(v_I * v_F)`.

The resulting 2x2 working sampling covariance must be positive definite and the variance of `g_I - g_F` must be positive.

## Programme-cluster state-separation test

For each of the three species, compute the covariance-aware `I - F` contrast and its two-sided Normal p-value.

Because the species share the same four landscapes and are not independent primary systems, ML020 receives **one conservative programme-cluster p-value**:

`p_ML020 = min(1, 3 * min(p_Atamisquea, p_Cercidium1990, p_Prosopis1990))`.

This is a within-programme Bonferroni gate. It does not treat the three species as independent Fisher inputs.

## Admission gate

Promote ML020 to `admissible_multilayer_cluster` only if:

1. all three species have exact four-site PT and FS habitat-unit mean vectors for continuous and small fragments;
2. every marginal effect uses site-specific habitat-unit means, never individual-level pseudo-replication;
3. each species' PT/FS covariance proxy is reconstructable and valid;
4. the common endpoint/year/species rules above are applied without post-hoc substitutions;
5. one programme-cluster p-value is produced as specified above.

Admission is based on design/effect-unit validity, not significance.

## Confirmatory diagnostic

After admission only:

- add ML020 as one fifth primary Hedges-g cluster;
- recompute the full primary Fisher combination;
- recompute all leave-one-primary-cluster-out diagnostics;
- treat `omit ML001 Serapias` as the key scientific test.

If omission of ML001 remains non-significant, record that as failure of Serapias-independent robustness. If it rejects, report that the conclusion survives removal of ML001 in a fifth, independently structured fragmentation programme while preserving the retrospective discovery limitation above.