# CF01_GPAIR_002 Prunus africana recovery — 2026-09-19

## Decision

Yineger et al. (2014) contributes one **pair-specific covariance-aware Phase-2 cluster** to `G_adult-G_offspring`.

It does **not** enter the frozen Phase-1 five-cluster Fisher synthesis.

This is a retrospective external recovery because the open article table was visible during candidate discovery. All eight source patches and the predeclared `H_S` endpoint are retained regardless of result.

## Fixed frame

Independent unit = forest patch.

- fragmented/small: Demba, Dishi, Metin, Temcha;
- reference/large: Bradi, DarabaSigsi, Kambo, Wonse.

Thus the direct comparison is 4 independent small patches versus 4 independent large patches.

The source's isolation classification is retained as metadata/sensitivity only and does not replace patch size.

## Recovered effects

Using the canonical direct EGWEE Hedges-g estimator:

| layer | small mean | large mean | Hedges g | sampling variance |
|---|---:|---:|---:|---:|
| G_adult, adult H_S | 0.7535 | 0.7845 | -1.275951575 | 0.601753276 |
| G_offspring, seedling H_S | 0.7000 | 0.72725 | -0.834579036 | 0.543532635 |

Both marginal effects point toward lower gene diversity in small patches. This direction was not used for admission.

## Adult–offspring geometry

After residualizing adult and seedling `H_S` on the fixed large/small exposure:

- residual correlation = `0.621977955`;
- reconstructed covariance = `0.355710788`;
- paired covariance eigenvalues ≈ `0.21574300`, `0.92954291` → positive definite.

The prespecified contrast is:

`G_adult - G_offspring = -0.441372539`

with:

- variance = `0.433864336`;
- SE = `0.658683790`;
- z = `-0.670082588`;
- two-sided p = `0.502805144`;
- 95% CI = `[-1.732369045, 0.849623967]`.

The interval crosses zero, so this programme does not resolve a cohort-specific fragmentation response. It still supplies an independent same-exposure adult/offspring programme and therefore increases information without selecting on state-separation significance.

## Phase-2 consequence

With this programme, direct `G_adult-G_offspring` coverage becomes **4 independent programmes**:

- ML003;
- P2_SF05_93 Parkia;
- P2_SF05_71 Heliconia;
- P2_CF01_GPAIR_002 Prunus.

The preregistered opening gate is **5 independent programmes**, so the cross-system G-pair meta-analysis remains closed at **4/5**.

Afrocarpus remains a registered prospective candidate but is not counted because exact population-level adult/progeny uHe values have not yet been recovered from a legitimate public source.
