# Phase-2 SF05-93 Parkia recovery — 2026-09-19

## Decision

Lompo et al. 2020 (*Parkia biglobosa*) now contributes one **pair-specific covariance-aware Phase-2 cluster** for `G_adult-G_offspring`.

It does **not** enter the frozen Phase-1 five-cluster Fisher synthesis.

## Fixed frame

The prerecovery contract fixes population as the independent unit and the source-defined higher-fragmentation cotton populations as the fragmented group:

- fragmented / CP: Walley, Vouza;
- reference / NCP: Saki, Cassou.

The locked primary endpoints are:

- `C`: NMπ pollen immigration rate;
- `G_adult`: large-tree expected heterozygosity `H_E`;
- `G_offspring`: embryo expected heterozygosity `H_E`.

Adults, embryos, maternal trees and loci remain nested observations and never increase fragmentation-level n.

## Recovered marginal effects

Using the canonical EGWEE direct Hedges-g estimator with two independent populations per exposure group:

| layer | fragmented mean | reference mean | Hedges g | sampling variance |
|---|---:|---:|---:|---:|
| C | 47.000 | 54.000 | -0.199750468 | 1.004987531 |
| G_adult | 0.815 | 0.805 | 0.808122036 | 1.081632653 |
| G_offspring | 0.800 | 0.785 | 0.766651878 | 1.073469388 |

Negative C therefore means lower pollen-immigration support in the higher-fragmentation group under the fixed orientation. Both genetic-state marginal effects are slightly positive on this standardized four-population contrast. These signs were not used for admission.

## Dependence result

All three endpoints share the same four populations. Residual correlations were reconstructed after removing the fixed CP/NCP group means and mapped onto the audited marginal variances.

The resulting three-layer working covariance matrix is **rank deficient (rank 2)**. With four populations and two fitted group means, only two residual degrees of freedom remain, so a 3×3 residual-correlation matrix cannot support a full three-layer joint inversion.

This is retained as a declared limitation rather than repaired numerically.

The prespecified `G_adult-G_offspring` 2×2 block is positive definite:

- residual correlation = 0.316227766;
- covariance = 0.340749107;
- eigenvalues ≈ 0.73677747 and 1.41832457.

Therefore Parkia is admissible for the pair-specific `G_adult-G_offspring` family while the C/G/G three-layer joint cluster remains non-admissible.

## Coverage change

The direct `G_adult-G_offspring` family increases from:

- **1 independent programme:** ML003

to:

- **2 independent programmes:** ML003 + P2_SF05_93.

The preregistered analysis-opening gate remains **5 independent programmes**, so this pair is still descriptive/developmental and no cross-system pair meta-analysis is opened.

## Reproducibility files

- `manuscript/SF05_93_PARKIA_PHASE2_RECOVERY_CONTRACT.md`
- `evidence/meta_extraction/phase2_sf05_93_parkia_population_values_v1.csv`
- `evidence/meta_extraction/phase2_sf05_93_parkia_effects_v1.csv`
- `evidence/meta_extraction/phase2_sf05_93_parkia_covariance_v1.json`
- `scripts/check_phase2_sf05_93_parkia.py`

The checker recomputes all three marginal Hedges-g effects, the residual-correlation matrix, the working covariance matrix, the full-rank failure and the positive-definite genetic pair block from the population-level source values.
