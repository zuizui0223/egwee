# ML018 / PS023 Spondias mombin cluster-recovery contract

**Locked before extracting the population-level numeric effect vectors used for synthesis.**

## Goal

Test whether the Nason & Hamrick *Spondias mombin* fragmentation study can supply a fifth independent **primary direct Hedges-g multilayer cluster** under the frozen EGWEE effect-family rules.

The confirmatory target remains whether primary state separation survives omission of `ML001 Serapias`. Admission is based on design/effect-unit validity, not on whether ML018 makes the Fisher p-value smaller.

## Source

Nason JD, Hamrick JL. 1997. *Reproductive and Genetic Consequences of Forest Fragmentation: Two Case Studies of Neotropical Canopy Trees.* Journal of Heredity 88:264–276. DOI: 10.1093/oxfordjournals.jhered.a023104.

Only the *Spondias mombin* component is eligible for ML018. The Ficus case studies are different species/pollination systems and are not pooled into this cluster.

## Frozen biological comparison

Use the source-defined fragmentation classes in the Barro Colorado / Gatun Lake landscape:

- fragmented/exposed = **small island-fragment S. mombin populations**;
- reference = the source's **large-fragment and continuous-forest S. mombin populations** used in the same 1994 comparison.

The primary synthesis frame is the intersection of source-defined populations for which both prospectively fixed endpoints below were actually measured. Missing endpoints do not become zeros. Joint availability may reduce the population set, but no population may be included/excluded because of its response value or significance.

The exact population IDs in that common frame must be recovered from the source before calculating either Hedges g. The named FDP, LC and DL populations may enter the reference group only if the primary source confirms that they belong to the same comparison and have both retained endpoint values.

Do not replace the source grouping with a post-hoc threshold in island area, isolation distance, adult density, fruiting-tree number, or pollen-flow magnitude.

## Independent effect unit

The independent fragmentation unit is the **population / forest fragment**.

Maternal trees, fruits, seeds, progeny and allozyme loci are nested below population. They are not fragmentation replicates and must not be used as Hedges-g n.

Admission requires at least two biological layers represented by one value per population on an aligned population frame.

## Prospectively fixed primary layers and endpoint hierarchy

### C_movement_connectivity

Primary endpoint: **population-level total/apparent pollen immigration (interpopulation pollen gene flow)** estimated from the paternity-exclusion analysis.

Orientation: greater pollen immigration/connectivity is treated as greater movement support (`orientation_multiplier = +1`).

Do not replace this endpoint after numeric recovery with maternal-family paternity events, pollen distance, outcrossing rate, or a lower-level progeny count.

### F_reproductive_function

Primary endpoint hierarchy, fixed before population-level values are opened:

1. **population-level fruit production / fruiting success** used in the source fragmentation comparison, preferably the source's tree-size-adjusted population representation if exact population values are available;
2. only if item 1 is not numerically reconstructable at the population unit, **population-level seed germination success** may be used, provided it is available on the same population frame as C and its population-level variance/values are recoverable.

The hierarchy is based on biological proximity to realised reproductive function and effect-unit recoverability, not effect magnitude or significance. Once a higher-priority endpoint is numerically reconstructable, the lower-priority endpoint cannot replace it because it yields stronger state separation.

Orientation: higher fruit production or germination = greater reproductive support (`orientation_multiplier = +1`).

## Effect-size contract

The primary stream remains `hedges_g_direct`:

- calculate Hedges g for small-fragment minus reference populations;
- calculate means/SD/n from independent population-level values, not nested maternal trees or progeny;
- use the existing EGWEE `metafor::escalc(measure="SMD", vtype="LS")` variance semantics;
- store raw direction and orientation multiplier explicitly;
- do not transform the source paternity-event count or lower-level reproductive observations into pseudo-population Hedges g.

## Dependence / covariance rule

The same population IDs must be aligned across C and F.

If the paired population vectors are recoverable:

1. centre C and F within the frozen fragmented/reference groups;
2. estimate the paired-population residual correlation;
3. translate that correlation to covariance using the two Hedges-g sampling variances;
4. construct and verify a positive-definite 2x2 working V matrix.

Do not assume zero covariance. If exact paired vectors cannot be recovered, ML018 is not admitted under the current synthesis machinery merely because separate group means or significance tests exist.

## Admission gate

Promote to `ML018 admissible_multilayer_cluster` only if all hold:

1. the source-defined small-fragment versus large/continuous comparison is recoverable without outcome-dependent recoding;
2. population is preserved as the independent fragmentation unit;
3. exact population IDs and numeric C values are recoverable for the pollen-immigration endpoint;
4. the fixed F endpoint hierarchy yields an exact population-level vector on the same biological comparison;
5. at least two fragmented and at least two reference independent populations remain on the common C/F frame;
6. Hedges-g sampling variances are based on population replication;
7. paired-population covariance is reconstructable and the working V is valid;
8. no population, endpoint, threshold, sign convention or layer mapping is changed after inspecting numeric state-separation results.

If any gate fails, record the blocker and leave ML018 outside the primary denominator.

## Confirmatory diagnostic after admission

Only after the admission gate is passed:

- add ML018 to the existing primary state-separation synthesis;
- recompute the full five-cluster Fisher combination;
- recompute every leave-one-primary-cluster-out diagnostic;
- treat **omit ML001 Serapias** as the confirmatory robustness question.

An admissible ML018 that does not make the Serapias-omission test significant remains a valid negative robustness result.