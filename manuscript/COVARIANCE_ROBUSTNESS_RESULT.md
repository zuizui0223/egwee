# Covariance robustness result

## Purpose

The primary state-separation test uses working within-cluster covariance proxies reconstructed from aligned independent units. This audit asks how much the cross-cluster conclusion relies on those covariance terms without changing any marginal Hedges-g effect or marginal sampling variance.

Three regimes are compared:

1. **Frozen paired covariance proxy** — the canonical analysis.
2. **Zero-covariance working sensitivity** — all within-cluster off-diagonal sampling covariances are set to zero while marginal effects and variances are unchanged.
3. **Cauchy–Schwarz covariance-free certification bound** — for every endpoint pair, use `Cov_ij = -sqrt(V_i V_j)`, the Cauchy–Schwarz lower covariance bound that maximises `V(g_i-g_j)` and therefore maximises the two-sided p-value for that pair. The resulting cluster p-values are conservative pairwise upper bounds. This is a certification boundary from marginal information alone, not a claim that all pairwise lower covariance bounds form one jointly realised covariance matrix.

The within-cluster all-pairs Bonferroni rule and the cross-cluster Fisher rule are unchanged in all three regimes. ML020 remains one programme cluster with a Bonferroni gate across its three dependent species-specific I–F tests.

## Results

| regime | ML001 | ML002 | ML003 | ML014 | ML020 | Fisher X | full p | omit-ML001 p |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Frozen paired covariance proxy | 0.00354530 | 0.19911670 | 0.17406774 | 0.09831774 | 1.00000000 | 22.64771647 | **0.01212432** | **0.18194353** |
| Zero covariance | 0.00197859 | 0.45532702 | 0.44464450 | 0.17480727 | 1.00000000 | 19.13332192 | **0.03860161** | **0.57123438** |
| Cauchy–Schwarz certification bound | 0.01192458 | 0.59635318 | 1.00000000 | 0.33712001 | 1.00000000 | 12.06678382 | **0.28061178** | **0.92060125** |

## Interpretation

The full five-cluster rejection is **not an artefact of requiring the fitted off-diagonal covariance proxies to be non-zero**: setting all off-diagonal covariances to zero still rejects the global null (`p=0.03860`).

However, the rejection is **not covariance-free**. If the analysis discards all paired dependence information and asks for a guarantee using only marginal effects/variances plus the Cauchy–Schwarz covariance bounds, the conservative Fisher p-value is `0.28061`. Thus the marginal effects alone do not certify a cross-cluster rejection for every covariance structure allowed by their variances.

The decisive biological influence result becomes stronger under both sensitivities. Omitting ML001 *Serapias* gives `p=0.57123` under zero covariance and a covariance-free certification bound of `p=0.92060`; neither is close to rejection.

The defensible claim is therefore:

> Under the prespecified paired-unit covariance reconstructions, the primary five-cluster corpus rejects complete layer exchangeability; the full rejection also survives a zero-covariance working sensitivity, but it cannot be certified from marginal effects alone when within-cluster covariance is left entirely unknown. In every dependence regime examined, the cross-system signal remains materially dependent on ML001 *Serapias*.

This sensitivity does not change cluster admission, marginal effects, the canonical primary result, or the search-stop rule. It narrows the evidential interpretation by making dependence information part of the stated condition for the strongest rejection claim.
