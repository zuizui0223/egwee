# ML016 / Aizen–Feinsinger 1994 *Atamisquea emarginata* recovery contract

## Purpose

Recover one fifth independent primary cluster in the already-frozen `hedges_g_direct` family, specifically to test whether the primary state-separation conclusion survives omission of `ML001 Serapias`.

The purpose is not to minimize the full-corpus p-value.

## Source

Aizen MA, Feinsinger P. 1994. Forest fragmentation, pollination, and plant reproduction in a Chaco dry forest, Argentina. *Ecology* 75:330–351. DOI 10.2307/1939538.

## Why this species is selected structurally

The paper contains several species and repeated-year observations. `Atamisquea emarginata` is selected because, before synthesis calculation, it satisfies the simplest non-overlapping frame:

- one flowering campaign rather than repeated years;
- all four replicated study sites represented;
- continuous forest, large fragment, and small fragment present at all four sites;
- the source states that, except for explicitly noted exceptions, pollen-tube, fruit-set, and seed-set data came from the same sampled individuals;
- Appendix I exposes site-by-habitat summary rows for both targeted layers.

This rule avoids selecting among species or years according to significance or effect magnitude. Prosopis and Cercidium repeated-year rows are not used to increase the independent denominator.

## Frozen primary exposure

Use the source-defined extreme direct contrast:

- fragmented = small forest fragment `<1 ha`;
- reference = continuous forest;
- large fragments (`>2 ha`) are retained as an ordered sensitivity/generalisation condition and do not define the primary two-group Hedges-g effect.

The four study sites are the independent landscape replicates. Individual plants are nested within site × habitat unit and are not used as the primary n.

## Frozen layers

Two primary effects only:

1. `I_interaction`: mean pollen tubes per flower/style (`PT`), interpreted as realised pollination success/effectiveness.
2. `F_reproductive_function`: fruit set (`FS`; fruits per flower, or source-appropriate floral unit).

Do not substitute pollen grains, seed set, seed output, or a different species because their results are more favourable.

## Effect-unit rule

For each layer, take the four published site-specific habitat-unit means in Appendix I as the observations:

- continuous forest: one site mean per site;
- small fragment: one site mean per same site.

Thus `n_ref = 4` and `n_frag = 4` for the primary effect. The within-site plant counts and within-site SDs document the precision of each site mean but do not increase the fragmentation replication count.

The primary SMD is computed with the existing EGWEE Hedges-g / `metafor::escalc(measure="SMD", vtype="LS")` semantics from the four site means per arm. Fragmented minus reference is oriented so negative values mean lower support/function under fragmentation.

## Pairing and dependence

The design is site-matched. Store the paired four-site vectors for both layers. The canonical primary Hedges-g calculation remains in the existing direct effect family; site pairing is used to reconstruct cross-layer and sensitivity dependence rather than treating plant-level observations as independent habitat replicates.

Because only four site pairs exist, any full covariance object is expected to be low-information. Use the existing lower-dimensional / conservative cluster handling rather than forcing an unstable inverse.

## Admission gate

Admit ML016 only if all are true:

1. the four site means for PT are completely recoverable for continuous and small-fragment habitat units;
2. the four site means for FS are completely recoverable on the same four sites;
3. no plant-level n is promoted to fragmentation replication;
4. the effect calculations reproduce independently under the frozen Hedges-g semantics;
5. the resulting two effects and site-paired dependence object are finite and auditable.

Admission does not depend on either layer effect, the within-cluster contrast, or the cross-cluster Fisher synthesis being statistically significant.

## Confirmatory robustness test

Only after admission:

- add ML016 to the primary cluster set;
- recompute the full Fisher combination using the same cluster-level state-separation p construction;
- recompute every leave-one-primary-cluster-out result;
- treat `omit ML001 Serapias` as the target robustness diagnostic.

A non-significant omit-ML001 result is a valid negative robustness outcome and must not trigger endpoint/species substitution.

## Outcome-visibility note

This recovery is not a fully outcome-blind prospective study: the 1994 publication and its qualitative findings are public and were visible during candidate discovery. The protection here is narrower and explicit: species/year/exposure/effect-unit/layer choices are fixed by structural completeness before the fifth-cluster synthesis is calculated, and no candidate is selected by its eventual contribution to the Fisher p-value.
