# ML019 / PS024 Pithecellobium elegans cluster-recovery contract

**Locked before population-level numeric endpoint recovery.**

## Goal

Test whether Hall, Walker & Bawa (1996) can supply a fifth independent **primary direct Hedges-g multilayer cluster** under the frozen EGWEE effect-family contract.

The confirmatory question is whether primary state separation survives omission of `ML001 Serapias`. Admission is based on the design/effect-unit contract and is not conditional on the full-corpus or leave-Serapias-out p-value becoming smaller.

## Source

Hall P, Walker S, Bawa KS. 1996. *Effect of Forest Fragmentation on Genetic Diversity and Mating System in a Tropical Tree, Pithecellobium elegans.* Conservation Biology 10:757–768. DOI: 10.1046/j.1523-1739.1996.10030757.x.

The source programme compares eight Costa Rican populations: two continuous populations in a 1500-ha reserve and six fragmented populations separated by up to 75 km. Published syntheses independently report that the same source includes adult/seed allozyme responses and reproductive fruit/seed-set responses across this two-versus-six population design.

## Frozen exposure

Primary direct contrast:

- fragmented/exposed = the six source-defined fragmented populations;
- reference = the two source-defined continuous populations in the 1500-ha reserve.

Do not redefine fragmentation using population size, distance from the reserve, geographic isolation, flowering density, genetic diversity, or reproductive outcome. Those quantities may be biologically informative moderators/descriptors but are not allowed to select the primary groups after outcome recovery.

## Independent effect unit

The independent fragmentation unit is the **population**.

Trees, flowering observations, fruits, seeds, progeny and loci are nested below population and are not primary replication units. Hedges-g means, SDs and n must therefore be calculated from one value per population for each retained endpoint.

Admission requires a common population frame with at least two independent fragmented populations and both independent reference populations represented in each retained layer.

## Prospectively fixed primary endpoints

### G_adult

Primary endpoint: **adult expected heterozygosity / gene diversity (`H_e`, or the source's directly equivalent expected-heterozygosity population statistic)** for each of the eight populations.

Rationale: this is a canonical standing adult genetic-diversity quantity, maps unambiguously to `G_adult`, and published summaries indicate that population-specific heterozygosity is reported across the eight-population fragmentation design.

Orientation: greater adult gene diversity = greater biological/genetic support (`orientation_multiplier = +1`).

Do not substitute percent polymorphic loci, effective number of alleles, population differentiation, distance from the reserve, or an outcome-selected genetic statistic after numeric recovery. If the exact expected-heterozygosity vector is not recoverable, ML019 does not switch to a different G metric merely because that metric is significant.

### F_reproductive_function

Primary endpoint hierarchy, fixed before numeric recovery:

1. **population-level seed set / seed-crop success**, where the source provides one quantitative reproductive value per population on the same eight-population comparison;
2. only if item 1 is not represented numerically at population level, **population-level fruit set / fruiting success** may be used, provided it is available on the same population frame and is quantitatively reconstructable without tree-level pseudo-replication.

The hierarchy is biological and unit-based, not significance-based. Once the higher-priority population-level endpoint is recoverable, it cannot be replaced by the lower-priority endpoint because of effect magnitude.

Orientation: higher seed/fruit set = greater reproductive support (`orientation_multiplier = +1`).

Temporal flowering proportion is a mechanistic/context variable rather than the primary F endpoint. A tree failing to fruit is not independently counted as a population replicate.

## Effect-size contract

The primary stream remains `hedges_g_direct`:

- calculate Hedges g for fragmented minus continuous groups from population-level values;
- use independent-population n (`6` fragmented, `2` reference) or the exact common-frame counts if the source documents endpoint-specific missing populations;
- use the existing EGWEE `metafor::escalc(measure="SMD", vtype="LS")` sampling-variance semantics;
- store raw direction and orientation multiplier explicitly;
- do not use numbers of trees, fruits, seeds, progeny or loci as Hedges-g n.

The two-reference-population design is small and therefore intrinsically imprecise; that is accepted as part of the design rather than repaired with lower-level pseudo-replication.

## Dependence / covariance rule

The G and F population vectors must be aligned by exact population identity.

If paired population vectors are recoverable:

1. centre G and F within the frozen fragmented/reference groups;
2. estimate the paired-population residual correlation;
3. translate that correlation to covariance from the two Hedges-g sampling variances;
4. construct and verify a positive-definite 2x2 working V matrix.

Do not assume zero covariance. If exact population-level F values or identities cannot be recovered, a qualitative statement that fragmented populations had lower seed/fruit set is insufficient for primary admission.

## Admission gate

Promote to `ML019 admissible_multilayer_cluster` only if all hold:

1. the source-defined six-fragment versus two-continuous exposure is recoverable without outcome-dependent recoding;
2. exact population identities are recoverable;
3. the fixed adult expected-heterozygosity vector is recoverable at population level;
4. the fixed F hierarchy yields an exact population-level reproductive vector on the same biological comparison;
5. at least two fragmented and both reference populations remain in the common G/F frame;
6. both Hedges-g effects and variances use population replication;
7. paired-population covariance is reconstructable and the working V is valid;
8. no endpoint, population, threshold, sign convention or layer mapping is changed after numeric state-separation results are inspected.

If any gate fails, record the exact blocker and leave ML019 outside the primary denominator.

## Confirmatory diagnostic after admission

Only after the admission gate is passed:

- add ML019 to the canonical primary state-separation synthesis;
- recompute the full five-cluster Fisher combination;
- recompute leave-one-primary-cluster-out sensitivity for every cluster;
- treat **omit ML001 Serapias** as the key robustness diagnostic.

A valid ML019 that fails to make the Serapias-omission combination reject at 0.05 is still a valid independent negative robustness result.