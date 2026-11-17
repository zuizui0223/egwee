# SF06 paired mean versus local interaction–function mismatch — 17 November 2026

**Status:** post-outcome, exploratory **secondary sensitivity only**. Source-locked quantitative calculation. This is **not** a new independent study, not a new source search, not a confirmatory pooled test, and not an amendment to the frozen five-cluster/17-effect fragmentation primary estimand. It belongs to empirical `egwee`, not theory `egwe`.

## Why test this

The present EGWEE fragmentation synthesis contains three independent programme-level, representation-stable examples where reproductive function (`F`) is more negatively affected than measured interaction/pollen quantity (`I`): *Eucalyptus wandoo*, *Cardiopetalum calophyllum*, and Kakamega *Acanthopale pubescens*. These are **existence examples**, not an unbiased prevalence sample. Do they imply that the mean matched female-fitness response must also be more negative than the mean pollination response in the broader supplementary effect dataset?

The source Aguilar et al. paper **already established** average pollination/female-fitness deterioration and a positive correlation between them; we do not claim to discover those facts. The present comparison is a deliberately narrow check on extrapolating *existence of downstream-biased mismatches* into a *global average downstream excess*. It was performed **after effects were available** and is therefore descriptive.

## Frozen source, comparison and independent unit

- Source: Aguilar et al. (online 2024, 2025 volume), *Annals of Botany*, DOI [10.1093/aob/mcae076](https://doi.org/10.1093/aob/mcae076); previously materialized pair file `evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv`, Git **blob SHA-1** `80edf240425c0e4439a276176bc1996c651fab92`.
- Accessible public S1 covers **426 effect rows**, versus **500** hierarchical inputs reported in the paper: 74 are not reconstructed or imputed.
- Existing source-exact study/publication × species × land-use pair keys: **59**; habitat-fragmentation pairs with numeric endpoints: **55**, from **33 source publications**.
- Within each pair compute `Delta = d_F - d_I` where `d` is the **source Hedges d**. Negative `Delta` denotes a stronger **standardized** negative female-fitness effect than standardized pollination effect. It is **not** a raw seed-per-visit ratio or a biological transfer coefficient. Their denominators (endpoint SDs) differ.
- Preserve all 55 pairs. Treat the whole original **publication** as the uncertainty cluster; do not count multiple species in Aizen–Feinsinger or Aguilar (2005) as independent papers.
- Equal-pair mean; intercept-only publication CR1 standard-error check; 8,000 whole-publication bootstrap resamples, fixed seed 20261117; equal-publication alternative; leave-one-whole-publication-out.
- Within-pair `Cov(d_I, d_F)` is not available. **No inverse-variance meta-analysis of the paired difference or significance test of ecological equivalence is attempted.**

## Recomputed result

| Diagnostic | Result |
|---|---:|
| Mean observed `d_I` (55 exact pairs) | **−0.46353** |
| Mean observed `d_F` (same pairs) | **−0.47207** |
| **Equal-pair mean `Delta = d_F − d_I`** | **−0.00854** |
| Publication-cluster CR1 SE | **0.13458** |
| CR1 normal-reference 95% interval | **[−0.27232, +0.25524]** |
| **8,000 publication-cluster bootstrap 95% interval** | **[−0.29862, +0.21893]** |
| Equal-publication mean `Delta` | **−0.05343** |
| Equal-publication bootstrap 95% interval | **[−0.33405, +0.22140]** |
| Paired `Delta < 0` / `Delta > 0` | **29 / 26** |
| Leave-one-publication-out unweighted mean range | **[−0.12349, +0.06018]** |

**Result:** This accessible matched subset does **not resolve a single average stronger female-fitness response than pollination response** on the paired Hedges-d scale. The interval is wide and includes both meaningful negative and positive effects; this is **not equivalence evidence**. A pooled mean near zero is compatible with large *context-specific* divergences in either direction. The publication-LOO mean changing sign is an influence warning, not a falsification of the three source-verified downstream mismatches.

## Ecological inference and negative controls on overclaiming

1. The three downstream mismatch anchors are retained as local **paired-contrast** evidence. Their within-programme covariance-aware contrasts do not turn into a corpus-level prevalence claim.
2. A non-significant average of standardized differences **does not** show that all programmes have equivalent process/function responses or that pollination is biologically irrelevant. It is compatible with heterogeneous conversion of interaction response into reproductive success.
3. The external SF06 topology reports 12 minimum point-state mismatches from 54 constituent-sign-consensus pairs, but **only 3 pairs** have both marginal directions individually resolved at 95%, and **none** of those three is opposite-sign. Point-sign geometry is not robust proof of opposite causal effects.
4. Cross-endpoint Hedges-d differences depend on endpoint variability, extraction design and unknown within-pair covariance. The public-S1 74-effect shortfall, nonrandom included studies, large unequal publication contributions, and overlap with the EGWEE I–F corpus further prevent a population-level prevalence conclusion.
5. Preexisting scientific work already separates pollen quantity and quality, mating compatibility and seed output. The 2026 review [*Animal Pollination Under Human-Induced Rapid Environmental Change*](https://doi.org/10.1146/annurev-environ-121224-092446) discusses these mechanisms; this audit **does not identify** any of them.

**Paper-level synthesis candidate, only as a qualified supporting sentence:**

> The matched evidence does not establish a uniform corpus-average excess of reproductive over pollination damage, while three source-audited systems exhibit resolved downstream-biased process–function contrasts. Directional fragmentation harm can thus coexist with strong context dependence in the translation from observed interaction quantity into reproductive output.

The core EGWEE contribution remains the **fragmentation-specific insufficiency of interaction quantity as a stand-alone reproductive sentinel** in audited settings, not an invented new response–effect theory, a global average-amplification law, or a finding about *all* flowering plants.

## Provenance and exact reproducibility

- Python stdlib: `scripts/audit_sf06_mean_vs_mismatch_20261117.py`.
- Dedicated isolated GitHub Actions run: [44099478435](https://github.com/zuizui0223/egwee/actions/runs/44099478435), **success** on script+workflow commit `61e3bad66f0de7b61fb13c33b1e1bd4e0c33232b`.
- Derivative-only artifact: [sf06-paired-mean-derivative, artifact 14335701376](https://github.com/zuizui0223/egwee/actions/runs/44099478435/artifacts/14335701376). No new source rows redistributed.
- Reproduce: `python scripts/audit_sf06_mean_vs_mismatch_20261117.py`.
- Source table SHA-1 / 59/55/33 denominator / paired arithmetic / 29:26 census are runtime hard gates; any source drift fails closed.
- **No changes** to `manuscript/MULTILAYER_FRAGMENTATION_META_ANALYSIS.md`, source primary effects or CI submission-ready decisions.

## Next meaningful independent validation

Not additional within-SF06 point-sign slicing. A separately selected **original-observation**, independent-landscape dataset must simultaneously measure pollinator/pollen quantity, effective transfer (compatible pollen or paternity), reproductive output, and observation effort/resource state. The current PoMS same-day FIT–pan comparison is valuable for observation-method calibration but **does not measure those reproductive endpoints**, so it is not an independent functional confirmation. A complete or independent matched dataset would be needed before a genuine generalizable macroecological stage-translation model can be estimated.
