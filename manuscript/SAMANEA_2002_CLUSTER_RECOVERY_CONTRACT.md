# ML016 / PS021 Samanea saman cluster-recovery contract

**Locked before table-level numeric extraction.**

## Goal

Test whether *Samanea saman* can supply a fifth independent **primary direct Hedges-g multilayer cluster** under the already-frozen EGWEE effect-family contract. The purpose is not to reduce the combined p-value. The target diagnostic is whether the primary state-separation conclusion can survive omission of `ML001 Serapias` after adding one genuinely independent same-family system.

## Source

Cascante A, Quesada M, Lobo JJ, Fuchs EA. 2002. Effects of Dry Tropical Forest Fragmentation on the Reproductive Success and Genetic Structure of the Tree *Samanea saman*. Conservation Biology 16:137–147. DOI: 10.1046/j.1523-1739.2002.00317.x.

Public repository copy: Universidad de Costa Rica Kérwá repository, item `https://hdl.handle.net/10669/78988`.

## Frozen exposure

Use the source-defined binary tree condition only:

- fragmented/exposed = isolated individual trees, >500 m from the nearest conspecific and surrounded by agricultural fields, pastures, or small forest remnants;
- reference = trees in continuous populations, >=10 conspecific individuals per hectare and surrounded by undisturbed forest.

Do not replace this contrast with a post-hoc distance, density, seed-predation, or outcome-derived grouping.

## Independent effect unit

The candidate independent unit is the **maternal tree** when the source reports tree-level summaries for both conditions. Flowers, fruits, seeds, progeny, loci, and repeated seedling measurements are nested below maternal tree and must not be promoted to fragmentation replicates.

Admission requires that at least two eligible layers can be reconstructed on the same source-defined maternal-tree frame, or on clearly overlapping maternal-tree subsets with defensible covariance/dependence handling.

If the published analysis only exposes pooled condition-level summaries whose variance cannot be mapped back to the maternal-tree sampling frame, the cluster is not admitted merely because lower-level sample sizes are large.

## Prospectively targeted layers

The following layer mapping is fixed before table-level numbers are opened:

1. `I_interaction`: natural pollination / pollen-tube success, preferably a tree-level endpoint tied to pollen receipt or successful pollen-tube progression.
2. `F_reproductive_function`: realised reproductive or progeny-performance endpoint, with priority to germination or seedling growth/vigour when reported on the maternal-tree frame. Seed number is eligible only if its independent sampling unit is recoverable.
3. `G_offspring`: progeny mating/genetic state, prioritising effective self-fertilisation / inbreeding or another source-reported progeny genetic endpoint if an effect and sampling variance are reconstructable on the same maternal-tree frame.

No endpoint is promoted because it produces a stronger contrast. If multiple endpoints exist within one layer, select according to source hierarchy and effect-unit recoverability, not significance.

## Effect-size contract

The primary stream remains `hedges_g_direct`:

- calculate Hedges' g for isolated minus continuous conditions;
- orient so negative values mean fragmentation/isolation reduces biological support/function;
- for deterioration metrics where larger raw values mean worse state (for example selfing or inbreeding), store the raw sign and apply `orientation_multiplier=-1` exactly as in the frozen EGWEE protocol;
- use sampling variance consistent with the existing `metafor::escalc(measure="SMD", vtype="LS")` semantics when means/SD/n are recoverable.

Do not convert correlations, test statistics, proportions, odds ratios, or lower-level pseudo-replicated observations into Hedges g unless the conversion preserves the maternal-tree effect unit and is justified before outcome synthesis.

## Dependence / covariance rule

If two or more retained layer effects share maternal trees, reconstruct a paired/tree-level covariance proxy when the public source permits it. If covariance is not reconstructable, retain the cluster only if a prespecified cluster-robust or conservative lower-dimensional contrast is valid under the existing synthesis machinery. Do not assume independence among endpoints from the same trees.

## Admission gate

Promote to `ML016 admissible_multilayer_cluster` only if all conditions hold:

1. source-defined isolated-vs-continuous exposure is independent of outcomes;
2. at least two predeclared biological layers are recoverable in the primary `hedges_g_direct` family;
3. maternal-tree independent n and effect-size variance are recoverable without using flowers/fruits/seeds/progeny as fragmentation replicates;
4. the retained layers refer to the same biological comparison and sufficiently aligned maternal-tree frame;
5. within-cluster dependence can be reconstructed or handled by the already-declared conservative fallback;
6. no endpoint/layer choice is changed after seeing the recovered effect sizes.

If any gate fails, record the exact blocker and leave the fifth primary cluster unfilled. Do not rescue the system by moving it to the primary family from a different effect metric.

## Confirmatory diagnostic after admission

Only after admission and covariance construction:

- recompute the existing cluster-level state-separation diagnostic with ML016 added;
- report the full five-cluster Fisher combination;
- report leave-one-primary-cluster-out sensitivity for every cluster;
- treat `omit ML001 Serapias` as the key robustness diagnostic.

The scientific success criterion is **robustness to removal of ML001**, not a smaller full-corpus p-value. A fifth cluster that is admissible but leaves the ML001-omission result non-significant is still a valid negative robustness result.
