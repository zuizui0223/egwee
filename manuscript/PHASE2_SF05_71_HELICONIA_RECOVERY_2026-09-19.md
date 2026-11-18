# Phase-2 SF05-71 Heliconia recovery — 2026-09-19

## Decision

Côrtes et al. 2013 (*Heliconia acuminata*) contributes one **full covariance-aware three-layer Phase-2 cluster** on a common five-site fragmentation frame:

- C — pollen immigration;
- G_adult — reproductive-plant UHe;
- G_offspring — seedling UHe.

It does **not** enter or alter the frozen Phase-1 five-cluster Fisher synthesis.

## Fixed site frame

Independent unit = site.

- fragmented: F1, F2, F3, each a 1-ha forest fragment;
- reference: CF1, CF2, continuous forest.

Nested plants, seedlings, loci and parentage events are not fragmentation replicates.

## Locked endpoints

The recovery contract fixes the endpoints independently of the calculated effect directions:

- C = percentage of seedlings with father outside the sampled plot;
- G_adult = unbiased expected heterozygosity (UHe) of reproductive plants;
- G_offspring = UHe of seedlings.

Plant density is not substituted for the source fragment/reference exposure.

## Recovered marginal effects

| layer | fragmented mean | reference mean | Hedges g | sampling variance |
|---|---:|---:|---:|---:|
| C | 20.6667 | 10.5000 | 0.996495431 | 0.932633648 |
| G_adult | 0.6960 | 0.6570 | 0.943012858 | 0.922260658 |
| G_offspring | 0.6893 | 0.6590 | 0.626928687 | 0.872637291 |

The signs are reported descriptively and were not used for admission.

## Covariance result

The three site-level endpoints were residualized on the fixed fragment/continuous indicator and the residual-correlation matrix was mapped onto the canonical marginal variances.

The resulting 3×3 working covariance matrix is **positive definite**:

- determinant ≈ 2.8972e-05;
- minimum eigenvalue ≈ 1.3714e-04.

No ridge or zero-covariance rescue was used.

The G_adult-G_offspring 2×2 block is also positive definite, with residual correlation 0.912396581.

## Coverage change

The direct G_adult-G_offspring family increases from 2 to **3 independent programmes**:

- ML003;
- P2_SF05_93 Parkia;
- P2_SF05_71 Heliconia.

The preregistered pair-specific analysis-opening gate remains **5 independent programmes**. The family therefore remains below the quantitative meta-analysis gate at 3/5.

## Reproducibility

- `manuscript/SF05_71_HELICONIA_PHASE2_RECOVERY_CONTRACT.md`
- `evidence/meta_extraction/phase2_sf05_71_heliconia_population_values_v1.csv`
- `evidence/meta_extraction/phase2_sf05_71_heliconia_effects_v1.csv`
- `evidence/meta_extraction/phase2_sf05_71_heliconia_covariance_v1.json`
- `scripts/check_phase2_sf05_71_heliconia.py`

The checker reconstructs all marginal effects and the covariance matrix from the five source site values.
