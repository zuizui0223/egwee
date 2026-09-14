# ML014 / Eucalyptus socialis 2012 effect-unit audit

**Audit date:** 2026-09-15

## Question

Can the Monarto maternal families in Breed et al. (2012), DOI `10.1111/mec.12056`, legitimately serve as the independent observational units for the ML014 fragmented-versus-reference Hedges-g contrast, or would that inflate one fragmented landscape versus one reference landscape in the same way rejected for ML009 *Pistacia lentiscus*?

## Source design

The source does **not** compare one fragmented site against one independent continuous site inside Monarto. Instead, all 29 Monarto mothers occur within the same broad landscape and are classified by the local landscape context of each sampled maternal tree:

- 13 low-density isolated-pasture mothers;
- 16 medium-density small-remnant-woodland mothers.

The article states that isolated-pasture mothers occurred in very small vegetation clusters, often as single trees, while small-remnant mothers occurred in natural woodland remnants surrounded by agriculture. Sampling of near-neighbour mothers was explicitly avoided, and a pairwise maternal-plant distance matrix is supplied in Appendix A. The authors explicitly prioritize the within-Monarto low- versus medium-density comparison because all of those trees belong to the same landscape, reducing site-level environmental confounding relative to the Yookamurra comparison.

The source also estimates mating-system quantities at family level and analyses family-level mating parameters against progeny growth. ML014 therefore uses a source-native maternal-family observational frame rather than expanding one site-level summary with offspring or locus counts.

## Why this differs from ML009 Pistacia

`ML009 Pistacia` has one highly fragmented landscape and one continuous reference stand. The fragmentation treatment is assigned at the landscape/stand level; mothers and seeds are nested below those two exposure units. Mothers therefore cannot become fragmentation replicates.

`ML014 Eucalyptus socialis` is different: within one Monarto landscape, the source assigns each sampled maternal tree to a local context (`isolated pasture` versus `small remnant woodland`). The primary comparison is variation among spatially separated maternal families carrying those source-defined local contexts. Progeny, repeated growth observations and loci remain nested below family and are never counted as independent exposure units.

## Admission decision

Retain ML014 as an `admissible_multilayer_cluster` with maternal family as the independent **observational** unit for this within-landscape local-context contrast.

This admission is conditional on the following claim ceiling:

1. ML014 is not described as a replicated landscape experiment.
2. The Hedges-g variance treats sampled maternal families as independent observational units after the source's near-neighbour avoidance; it does not prove absence of all residual spatial correlation.
3. No progeny, locus or repeated-measure count can increase `n` beyond the 13 fragmented and 15 public complete-case reference families.
4. Yookamurra remains excluded from the primary contrast because adding a second site would reintroduce cross-site environmental differences the source itself treats cautiously.
5. If future source information shows that the admitted families collapse to fewer independent exposure units than the maternal-tree frame implies, ML014 must be reclassified rather than rescued with family-level pseudo-replication.

## Current quantitative consequence

No effect value changes in this audit. The admitted complete-case frame remains 13 isolated-pasture versus 15 small-remnant families, with the already frozen endpoints:

- `G_mating`: family correlated paternity `r_p`, oriented as mating support;
- `F`: family mean progeny growth.

The audit clarifies the estimand and independence claim only. It does not strengthen the numerical evidence or remove the existing leave-one-primary-cluster-out sensitivity showing that ML001 remains influential.
