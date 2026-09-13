# ML015 / PS019 Eucalyptus wandoo 2018 recovery result

## Terminal state

`ML015_admitted_I_F_Gadult_covariance_aware`

ML015 is admitted as the fourth independent covariance-aware multilayer cluster.

## Locked frame

- source populations defining exposure geometry: 19;
- common response-complete populations: 11 (`J,K,F,C,E,G,B,I,A,H,D`);
- independent unit: population;
- exposure: response-free PC1 of source-defined fragmentation variables after fixed transforms `-log10(size)`, `sqrt(isolation)`, `log10(shape)`;
- biological layers: pollen tubes (`I`), seeds/fruit y2 (`F`), adult unbiased expected heterozygosity `H_e` (`G_adult`).

The aggregate source tables were visible during candidate discovery, so this is not described as an outcome-blind preregistration. Predictor reduction nevertheless uses exposure values only and no endpoint-specific predictor selection.

## Fragmentation PC

PC1 loadings after severity orientation:

- smallness `-log10(size)`: `+0.5873571692`;
- `sqrt(isolation)`: `+0.4775526468`;
- edge dominance `log10(shape)`: `+0.6534179561`.

PC1 eigenvalue: `1.8276073487`.

Higher PC1 therefore means smaller, more isolated and more edge-dominated populations.

## Layer effects

Each response was standardized once on the common 11-population frame. Effects are OLS slopes on fixed standardized fragmentation PC1. Negative means deterioration with stronger fragmentation; positive means an increase.

- `I_pollination`, pollen tubes at base of style: `+0.67475197`; bootstrap 95% CI `[+0.20780667, +1.93297843]`.
- `F_reproductive_function`, seeds per fruit y2: `-0.79455522`; bootstrap 95% CI `[-1.42507278, -0.22907996]`.
- `G_adult`, `H_e`: `-0.43933127`; bootstrap 95% CI `[-1.59705553, +0.22305372]`.

The important state geometry is therefore discordant: pollination quantity rises along the fragmentation-severity axis while realised reproductive function falls; standing adult genetic diversity is weaker and uncertain in the same deterioration direction.

This does not imply that more pollen is beneficial under fragmentation. The source itself argues that small populations can receive abundant pollen while seed set remains low, consistent with reduced pollen quality / increased self-pollen rather than pollen quantity limitation.

## Dependence

Paired population bootstrap: 10,000 draws, RNG seed `20260913`.

Bootstrap covariance matrix in endpoint order `[I_pollen_tubes, F_seeds_per_fruit_y2, G_adult_He]`:

```
[[ 0.1934720631,  0.0209037444, -0.0911208842],
 [ 0.0209037444,  0.0867636966,  0.0404803321],
 [-0.0911208842,  0.0404803321,  0.2287153403]]
```

Eigenvalues: `[0.0568871989, 0.1466268969, 0.3054370042]`.

All are positive, so the covariance matrix is positive definite and the predeclared admission gate is passed.

## Claim ceiling

ML015 supports a natural-system state-separation claim: a common multidimensional fragmentation state does not force pollination quantity, reproductive function and standing genetic diversity to move as one deterioration coordinate.

It does not identify a single causal fragmentation component, because the primary exposure deliberately summarizes the three source-defined fragmentation variables without choosing among them based on endpoint results. Soil salinity and pollen quality remain mechanistic explanations discussed by the source rather than components of the primary fragmentation estimand.
