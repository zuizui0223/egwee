# ML017 / PS022 Picea glauca cluster-recovery contract

**Locked before further stand-level numeric outcome recovery.**

## Goal

Test whether the linked 2006 white-spruce programme can supply the fifth independent **primary direct Hedges-g multilayer cluster** under the already-frozen EGWEE effect-family contract.

The confirmatory purpose is whether the primary state-separation conclusion survives omission of `ML001 Serapias`. A smaller full-corpus p-value is not the objective and is not an admission criterion.

## Source programme

Treat the following linked papers as **one biological cluster**, not two independent studies:

1. O'Connell LM, Mosseler A, Rajora OP. 2006. *Impacts of forest fragmentation on the reproductive success of white spruce (Picea glauca).* Canadian Journal of Botany 84:956-965. DOI: 10.1139/b06-051.
2. O'Connell LM, Mosseler A, Rajora OP. 2006. *Impacts of forest fragmentation on the mating system and genetic diversity of white spruce (Picea glauca) at the landscape level.* Heredity 97:418-426. DOI: 10.1038/sj.hdy.6800886.

Both reports derive from the same northern-Ontario landscape programme and the same 23 sampled stands / 104 maternal trees. Endpoints across the two papers therefore remain dependent observations inside one `ML017` cluster.

## Frozen exposure

Use the source-defined stand-size classes and a predeclared extreme-class direct contrast:

- fragmented/exposed = **small stands**, `1 to <10` white-spruce trees;
- reference = **large stands**, `>=100` white-spruce trees;
- medium stands (`10 to <100`) are excluded from the confirmatory primary Hedges-g contrast and may be retained only as a separately labelled sensitivity/gradient context.

This contrast is fixed before recovering the stand-level endpoint vectors. Do not choose a different threshold from reproductive or genetic outcomes, and do not replace stand-size class with post-hoc isolation distance, fitted stand size, or outcome-selected fragmentation geometry.

## Independent effect unit

The independent fragmentation unit is the **stand**.

Maternal trees/families, cones, seeds, embryos, loci and repeated measurements are nested below stands and must not be promoted to fragmentation replicates. The primary small-versus-large Hedges-g effects must therefore be calculated from one source-defined value per stand for each retained endpoint.

The target aligned primary frame is the source-defined 11 small plus 6 large stands. If an endpoint is not recoverable on that stand frame, do not substitute family/seed n. Any missing-stand reduction must be source-documented and declared before effect calculation; otherwise the candidate closes.

## Prospectively fixed primary endpoints

### F_reproductive_function

Primary endpoint: **stand-level mean number of filled seeds per cone** from the reproductive-success study.

Rationale: this is a realised reproductive endpoint, is directly interpretable as support/function, and is not mathematically constructed from the mating-system endpoint below.

Orientation: higher filled-seed production = greater reproductive support, so `orientation_multiplier = +1`; fragmented minus reference should be negative when fragmentation reduces function.

Do not replace this endpoint after seeing effects with fruit set, cone abundance, seed emptiness, germination, or any other reproductive measure.

### G_offspring / G_mating

Primary endpoint: **stand-level multilocus outcrossing estimate `t_m`** from the mating-system study.

Rationale: `t_m` is a source-reported progeny mating-state quantity available at the stand level and maps to the predeclared offspring/mating genetic layer.

Orientation: higher outcrossing = greater mating/genetic support, so `orientation_multiplier = +1`.

` t_m - t_s`, primary selfing, effective pollen-donor number, allelic diversity, heterozygosity and inbreeding metrics are not eligible substitutes for the primary endpoint after numeric recovery. They may be retained as explicitly secondary/sensitivity descriptors only if recoverable without pseudo-replication.

## Effect-size contract

The primary stream remains `hedges_g_direct`:

- calculate Hedges' g from **stand-level** values for small minus large classes;
- use the same small/large stand contrast for both endpoints;
- calculate sampling variance with the existing EGWEE Hedges-g / `metafor::escalc(measure="SMD", vtype="LS")` semantics;
- store raw direction and orientation multiplier explicitly;
- no endpoint may be converted from a family-, cone-, seed-, embryo- or locus-level test statistic into a stand-level Hedges g merely to obtain a variance.

Published class-level SE values based on nested trees/families are not automatically treated as stand-level SDs. Admission requires reconstructable stand-level values or another source representation that preserves stand replication.

## Dependence / covariance rule

Admission requires exact stand identifiers for the retained F and G endpoints on the aligned small/large frame.

If both stand-level vectors are recoverable, estimate the within-cluster sampling covariance using the same group-centred paired-unit proxy logic already used for existing paired primary clusters:

1. align F and G by stand ID;
2. centre each endpoint within small/large class;
3. estimate paired-stand residual correlation;
4. translate that correlation to covariance using the two Hedges-g sampling variances;
5. verify that the resulting 2x2 working V matrix is positive definite.

Do not assume zero covariance. Do not digitize a plot to manufacture the primary stand vector unless a separate method amendment is frozen before digitization and validates recovery error independently of the observed state-separation result.

## Admission gate

Promote to `ML017 admissible_multilayer_cluster` only if all conditions hold:

1. the source-defined small-versus-large exposure can be represented without outcome-dependent recoding;
2. stand-level filled-seeds-per-cone values are recoverable for the primary F endpoint;
3. stand-level `t_m` values are recoverable for the primary G endpoint;
4. stand IDs align on a defensible common primary frame;
5. both Hedges-g effects and their variances use stand replication rather than nested biological observations;
6. within-cluster covariance is reconstructable under the frozen paired-stand rule and the working V is valid;
7. no endpoint, threshold or unit is changed after the recovered values are inspected.

If any gate fails, record the exact blocker and leave ML017 outside the primary denominator.

## Confirmatory robustness diagnostic

Only after admission:

- add ML017 to the existing cluster-level state-separation synthesis;
- recompute the full five-cluster Fisher combination;
- recompute leave-one-primary-cluster-out sensitivity for all clusters;
- treat **omit ML001 Serapias** as the key confirmatory diagnostic.

The scientific success criterion is whether the rejection survives removal of ML001. ML017 remains a valid empirical recovery even if that robustness test fails.