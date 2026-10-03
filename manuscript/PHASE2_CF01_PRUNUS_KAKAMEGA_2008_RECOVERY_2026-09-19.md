# CF01_GPAIR_003 Prunus africana Kakamega recovery — 2026-09-19

## Decision

Farwig et al. (2008) contributes one **pair-specific covariance-aware Phase-2 cluster** to `G_adult-G_offspring`.

It does **not** enter or alter the frozen Phase-1 five-cluster Fisher synthesis.

This is a retrospective external recovery because the public Table 2 was visible during candidate discovery. The admission rule retains all eight sites and the same `H_E` endpoint in both generations.

## Fixed frame

Independent unit = site/population.

- fragmented: Malava, Kisere, Ikuywa, Kaimosi;
- reference/main forest: Mukangu, Buyangu, Isecheno B, Isecheno A.

Adults and seedlings were sampled in spatially matched pairs within each site, but individual pairs remain nested. Fragmentation-level n is 4 versus 4.

## Recovered effects

Using the canonical direct EGWEE Hedges-g estimator:

| layer | fragment mean | main-forest mean | Hedges g | sampling variance |
|---|---:|---:|---:|---:|
| G_adult, adult H_E | 0.8100 | 0.7925 | +0.651343647 | 0.526515534 |
| G_offspring, seedling H_E | 0.7675 | 0.7400 | +0.677493106 | 0.528687307 |

The positive marginal signs mean the eight-site standardized contrast does not show lower expected heterozygosity in the fragment group for either cohort. These signs were not used for candidate retention or admission.

## Adult–offspring geometry

After residualizing both cohort endpoints on the fixed fragment/main-forest grouping:

- residual correlation = `0.646753411`;
- reconstructed covariance = `0.341227295`;
- covariance eigenvalues ≈ `0.18637263`, `0.86883021` → positive definite.

The prespecified pair contrast is:

`G_adult - G_offspring = -0.026149459`

with:
- variance = `0.372748250`;
- SE = `0.610531121`;
- z = `-0.042830673`;
- two-sided p = `0.965836513`;
- 95% CI = `[-1.222768468, 1.170469550]`.

Thus this programme provides essentially no resolved adult-versus-seedling difference in the fragmentation response. It is nevertheless the fifth independent same-exposure programme and was not selected for a positive cohort-separation result.

## Phase-2 consequence

Direct `G_adult-G_offspring` coverage is now **5 independent programmes**:

- ML003;
- P2_SF05_93 Parkia;
- P2_SF05_71 Heliconia;
- P2_CF01_GPAIR_002 Prunus Ethiopia;
- P2_CF01_GPAIR_003 Prunus Kakamega.

The preregistered **5-programme analysis-opening gate is now met** for this one pair family.

This opens the quantitative cross-programme `G_adult-G_offspring` synthesis. It does not automatically open any moderator analysis, which still requires at least 10 independent clusters, and it does not satisfy the separate requirement that the systematic search frame be complete before Phase 2 can supersede the frozen submission manuscript.
