# CF01_GPAIR_002 / Prunus africana 2014 Phase-2 recovery contract

**Locked:** 2026-09-19 before Prunus effects are written to the EGWEE evidence tables.

## Audit status

Source: Yineger, Schmidt & Hughes (2014), *Genetic structuring of remnant forest patches in an endangered medicinal tree in North-western Ethiopia*, BMC Genetics 15:31, doi:10.1186/1471-2156-15-31.

This is a **retrospective external recovery**. The open article table containing population-level genetic values was visible during candidate discovery. Therefore this recovery does not claim prospective outcome blinding. Admission is protected instead by a deterministic endpoint/exposure rule, retention of all source populations, and a fixed effect-unit contract. No endpoint or patch subset may be changed after calculation because of effect direction or significance.

## Target pair

Primary Phase-2 family: `G_adult-G_offspring`.

The paper reports adult and seedling genetic diversity on the same eight forest patches.

## Exposure and independent unit

Primary fragmentation exposure = the paper's source-defined **patch-size class**:

- fragmented = small patch (`S`);
- reference = large patch (`L`).

Primary independent unit = **forest patch**.

All eight source patches in Table 1 are retained:

- large/reference: Bradi, DarabaSigsi, Kambo, Wonse;
- small/fragmented: Demba, Dishi, Metin, Temcha.

Thus `n_fragmented = 4` and `n_reference = 4`.

Adult trees, seedlings, loci, and repeated allelic observations are nested and never increase fragmentation-level n.

The source also classifies patch isolation (`C` less-isolated; `I` isolated). Isolation is retained as a sensitivity/moderator variable only and is not substituted for patch size after seeing outcomes.

## Locked genetic endpoint

Primary endpoint in both cohorts = source Table 1 **gene diversity `H_S`**.

Rationale:

- `H_S` is the source population-level expected genetic-diversity measure available on every patch and both cohorts;
- it is the closest same-metric analogue to the expected-heterozygosity endpoints already used in the Phase-2 G family;
- using the identical metric in adults and seedlings makes the cohort contrast interpretable without cross-metric conversion.

Orientation multiplier = `+1`: larger `H_S` means greater genetic support.

Allelic richness, mean number of alleles, `F_IS`, population-specific `F_ST`, and migrant proportions remain sensitivity/descriptive quantities. They cannot replace `H_S` because they yield a more convenient result.

## Direct effect calculation

For each cohort use the frozen EGWEE direct Hedges-g rule with small patches as fragmented and large patches as reference:

- `d = (M_small - M_large) / s_p`;
- `df = n_small + n_large - 2`;
- `J = 1 - 3/(4df - 1)`;
- `g = J d`;
- `V(g) = 1/n_small + 1/n_large + g^2/[2(n_small+n_large)]`.

Dispersion is the across-patch SD within source patch-size classes. Individual tree/seedling sample sizes do not enter fragmentation-level n.

## Paired adult-offspring dependence

Adult and seedling `H_S` values are paired by the same eight patches.

Working dependence is reconstructed using the existing EGWEE paired-unit proxy:

1. residualize each cohort endpoint on the fixed large/small group means;
2. calculate Pearson correlation of the eight paired residuals;
3. map it to sampling covariance as `Cov = rho * sqrt(V_adult * V_seedling)`;
4. evaluate `G_adult - G_offspring` directly from the two marginal effects and covariance.

## Admission rule

The programme can enter the Phase-2 `G_adult-G_offspring` family if:

- all eight Table 1 rows reproduce exactly;
- patch-size labels are source-defined and fixed;
- adult and seedling `H_S` use the same eight-patch frame;
- Hedges-g effects and paired covariance are deterministically reproducible;
- no lower-level sample count is promoted to fragmentation n.

It contributes one programme only and does not enter the frozen Phase-1 five-cluster Fisher synthesis.
