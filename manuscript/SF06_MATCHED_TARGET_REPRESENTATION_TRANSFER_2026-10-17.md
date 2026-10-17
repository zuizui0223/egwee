# What is transferable from pollination to female reproductive fitness? A same-case, same-target representation audit (2026-10-17)

## Status and ecological problem

**Empirical EGWEE only**, not the separate EGWE/NEE theoretical project. **Post hoc**, published-data prediction diagnostic. The original 2025 pollination meta-analysis (Aguilar et al., *Annals of Botany*, doi:10.1093/aob/mcae076) already reports aggregate positive pollination–female-fitness association. Our narrower question is different: **does a pollination effect observed in a publication help forecast the female-fitness outcome in a wholly different publication, and is that answer stable to representing the endpoint as a continuous effect or only a directional point-sign?** No new field study, source replication or verified causal mechanism is claimed.

This diagnostic reuses a frozen public-S1 derivative, `evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv` with Git blob `80edf240425c0e4439a276176bc1996c651fab92`. It does not alter the five direct clusters, eight quantitatively matched I–F programmes, 16-programme evidence map or the established SF06 54-sign-pair denominator.

### Important denominator correction that prevents an unfair comparison

This source contains **59 physical paired published land-use rows**; **54** are habitat-fragmentation pairs with consensus lower/nonlower signs in both constituents; **55** are habitat-fragmentation pairs numerically eligible for continuous `d_I/d_F`. One numerically eligible row has mixed constituents and is *not* in the 54 sign-consensus frame. Never compare a continuous predictor assessed on 55 rows against a sign predictor assessed on 54 and attribute the difference to representation.

This audit evaluates **both** numeric and binary female targets **on exactly the same 54 sign-consensus rows from 32 source publications**, and separately **31 source-publication-disjoint rows from 23 publications** after removing sources overlapping the frozen EGWEE matched programmes. Every model in one target/frame is fitted and scored on the identical rows; publications, not species/effect rows, are held out together. Sources within the original meta-analysis may contribute multiple correlated taxa; rows are not independently sampled ecosystems.

## Exact matched target and predictor comparison

The four prediction rules are: (1) training-publication mean/intercept only, (2) the sign of `d_I` as `lower/nonlower`, (3) continuous pollination effect `d_I`, (4) both sign and magnitude. The source's constituent-consensus sign matches the sign of its aggregated numeric effect on this **selected 54-row** frame, so no divergent sign codings are mixed.

The numeric `d_F` target uses **within-fold standardized ridge regression** with penalty 1 and squared error; the `F` lower/nonlower target uses within-fold standardized **ridge-penalized logistic likelihood**, with Brier and log-loss scoring. Intercepts are unpenalized. These are not the same target or loss and their numerical scores must not be compared to one another.

### Continuous female reproductive effect target: cross-publication MSE, lower is better

| Pollination predictor | All 54 / 32 publications | Source-disjoint 31 / 23 publications |
|---|---:|---:|
| Training female mean only | **0.462895** | **0.623925** |
| Pollination lower/nonlower point-sign | **0.446734** | 0.657612 |
| Continuous quantitative pollination effect `d_I` | 0.452495 | **0.614103** |
| Both features | 0.457161 | 0.655462 |

The apparent predictor advantage **reverses under publication-overlap exclusion**: in all 54 sign alone reduces MSE by about 3.49% versus context and outperforms `d_I`; in the disjoint 31, direction alone is *worse than doing nothing* and a continuous quantitative effect offers only a small ~1.57% improvement over context. These are comparison-of-model-scores, not independent trait coefficients or a controlled ecological experiment. The smaller disjoint sample is nested and changes which publications are evaluated; one cannot conclude that sign information is intrinsically biologically unreliable while magnitude is intrinsically reliable.

### Binary female lower/nonlower point-sign target: Brier score, lower is better

| Pollination predictor | All 54 / 32 publications | Source-disjoint 31 / 23 publications |
|---|---:|---:|
| Training female lower-state frequency only | **0.176739** | **0.183269** |
| Pollination lower/nonlower point-sign | 0.181503 | 0.193949 |
| Continuous quantitative pollination effect `d_I` | 0.177584 | 0.190088 |
| Both features | 0.182034 | 0.196921 |

**Neither pollination representation improves binary female-state calibration over the source-heldout training-state baseline** in these simple logistic models on this exact matched dataset. This remains a **point-sign** comparison; original sampling intervals and unknown paired I/F covariance mean it is **not** a verified sign-change prevalence estimate. Only **three** original consensus pairs have both endpoints 95% resolved, and those three are concordantly lower/lower. Do not claim the other discordant point-signs prove statistically resolved biological reversals.

### Why the contrast is biologically meaningful — but limited

The observed relationship is **target-dependent**:
- An upstream pollination effect carries **some weak conditional information** about a continuous, heterogeneous downstream fitness effect, but its useful representation depends on the evaluated publication universe.
- The same information does **not** reliably distinguish lower versus nonlower female-fitness signs in an entirely new source publication, compared with knowing the baseline frequency.
- Breeding-system labels from the separate 49/26 case-matched audit also failed to improve on continuous pollination effect for held-publication numeric prediction. Trait susceptibility in a pooled ecological meta-analysis is not the same as *conditional functional diagnosis* when upstream change is already observed.

That is narrower and more defensible than the blanket assertion “pollination does not predict reproduction.” It also does **not** assert zero conditional biological information, a universal endpoint nonlinearity, or a new causal mechanism downstream of mating.

## Robustness: published study weighting and whole-source influence

Numeric female-effect prediction **is especially fragile in the source-disjoint subset** when publication rather than effect row is weighted equally at scoring time:

| Numeric-female target; equal weight to each held publication | Baseline | Pollination sign | Pollination magnitude |
|---|---:|---:|---:|
| All 54, 32 publications | **0.476869** | **0.461081** | **0.461772** |
| Source-disjoint 31, 23 publications | **0.576158** | 0.632719 | 0.583533 |

Thus the modest disjoint 31-pair **row-weighted** benefit of continuous `d_I` (0.623925→0.614103) **does not persist under equal-publication scoring** (0.576158→0.583533). Do not assert a robust disjoint continuous effect prediction improvement.

Re-run the *entire* publication-held-out exercise after deleting each distinct source publication in turn, **rather than just deleting an influential row**:

- In all 54 pairs, for the **numeric female effect**, direction-only beats baseline after **32/32** individual source deletions, as does magnitude-only (**32/32**); direction beats magnitude in **28/32** deletions, so magnitude is not uniformly more informative.
- In source-disjoint 31 pairs, direction-only is *worse* than baseline after **22/23** deletions; magnitude-only is *better* than baseline after **19/23**, but worsens after **4/23**, and its equal-publication MSE is worse even without source deletion.
- For the **binary female lower/nonlower point-sign**, in the full 54 both sign-only and magnitude-only are worse than baseline after **32/32** source deletions; in the disjoint 31, both are worse after **22/23**, with a single opposite deletion result.

These deletion fits **overlap massively** and are **not 32 or 23 independent ecological tests**. They only describe how the measured conditional predictive utility depends on the small set of published sources. A source-selected post hoc MSE winner is not a validated universal reproductive mechanism.

## Inference and falsification limits

- The public supplement pairs heterogeneous taxonomic and female-fitness endpoints, sometimes at different sites/years and with **unknown within-pair `d_I/d_F` covariance**; inverse-female-variance weighting, origin-study hierarchical modeling, or local mating-quality records could change rankings.
- `d_I` and `d_F` are standardized, so their effect magnitudes are affected by the variability and measurement design of their respective endpoints. Do not interpret a linear regression as a directly identified per-visit biological conversion efficiency.
- This 54/31 comparison is **post hoc and nested**; including known breeding-system traits further restricts to different 49/26 denominators, which must not be mixed here.
- Exact-source deletion and model shrinkage influence checks may reveal that a narrow score advantage is driven by a subset of papers; overlapping deletion fits are *diagnostics*, never independent binomial replications.
- The original publication already demonstrated average changes and aggregate correlations; the added question is held-source **incremental diagnostic sufficiency under specified prediction targets**. This has a prior-art ceiling: failure of visitation-to-fitness conversion is widely known, so novelty can only be in carefully validated out-of-publication transport, not the statement that stages differ.
- No source-known ecological cause is isolated. Missing variables include realized compatible mating and pollen provenance, self-fertilization, seed abortion, seed arrival, safe-site opportunity and observation detection.

## Reproducibility and status

- New checker: `scripts/audit_sf06_target_representation_transfer.py`. It checks the exact Git blob, 59 original physical rows, 54/31 fixed sign-consensus fragmentation rows, whole-source deletion, both outcome families, λ=0.25/1/4 sensitivity, and per-publication score influence.
- New workflow: `.github/workflows/sf06-target-representation-transfer.yml`. Detailed machine-readable result: `build/sf06_target_representation_transfer_v1.json` from the GitHub Actions artifact.
- Source-scoped CI **PASS**, complete frozen-blob and source-deletion checks: https://github.com/zuizui0223/egwee/actions/runs/39006084678 (the subsequent machine-readable deletion-field spelling tidy-up reruns the same checks). Headline score values were also separately reproduced from the pinned CSV by an independent code path.
- Frozen main baseline is unchanged. PR #52 stays **draft**; `submission_ready=false` remains required because the dated manuscript freeze hash is intentionally not reconciled with ongoing exploratory work.

## Next outcome-identifying ecological test

A meaningful advance beyond predicting published mixed endpoints would pair measured **compatible pollen / paternity and viable seed arrival** with subsequent **whole-patch recruitment** in the same reproductive episodes, controlling visitation detection, patch abundance, plant size and true available microsites. The decisive contrast is not whether any proxy correlates with later yield, but whether direct quality or opportunity variables improve **held-landscape** recruits and predict the effect of a randomized pollen versus safe-site intervention. Until such data exist, biological stage identity is underidentified.
