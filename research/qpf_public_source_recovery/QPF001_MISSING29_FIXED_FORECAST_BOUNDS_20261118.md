# QPF001 — sharp missing-fruit bounds on the original fixed-forecast Q→P→F comparison

**Status 2026-11-18: POSTHOC PARTIAL IDENTIFICATION, not a new preregistered hypothesis test or new positive ecological finding.** The original 2021 flower-level source experiment, original M0/M1 model, and original conclusion `NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN` are unchanged.

## Starting point and exact original evidence

Smith, Swartz & Spigler (2021), *American Journal of Botany*, DOI [10.1002/ajb2.1720](https://doi.org/10.1002/ajb2.1720); Dryad [10.5061/dryad.hqbzkh1g9](https://doi.org/10.5061/dryad.hqbzkh1g9). User-supplied original ZIP SHA256 `09a47a94913c7087405679c5dc18c0c3c6ded4e8ecad298e6f94f87c5a78b653`, original published XLSX SHA256 `83790bb7d63222e3e21c0ceed5d729cacf63a2df843e5807836d8e5c853447aa`. Both ZIP and inner XLSX provenance were verified.

The original preregistered model and raw-source analysis were merged by [PR #77](https://github.com/zuizui0223/egwee/pull/77), protocol commit `a1658c353a0c244edafab194f96301968dc84040`. It trained M0 on filmed visit rates/flower neighborhood/Julian day, and M1 with added source stigmatic CP and HP counts and previously known CP×HP interaction, on 93 recovered fruits. Eight entire filming dates were each held out. Recorded original MSEs: M0 **0.0945916595**, M1 **0.0932771749**, improvement **+0.0013144845** (1.39%) and 4/8 dates positive. The **5% and 6/8 registered success requirement failed**.

Independent source follow-up [PR #79](https://github.com/zuizui0223/egwee/pull/79) found a severe source selection and seasonal transport limitation: **29/122 filmed flowers had no recoverable mature fruit Seed.set**; 23/29 missing were filmed on only dates 176/178; the four recovered flowers on late date 196 alone accounted for essentially the entire positive originally scored model difference.

## What this audit computes

For each of the original eight held-out dates:

1. Train original, *unchanged* M0 and M1 only on originally recovered-source fruits from the **other seven dates**. Predictor definitions, training-only neighborhood imputation, training-only standardization, ridge λ=1 and [0,1] prediction clipping are unchanged.
2. Recompute **all 32 original date×model MSE and MAE values**, requiring exact agreement with the registered PR #77 results (within `1e−10`).
3. Extend the **same training-date fitted models** to the filmed flowers with **unobserved fruit outcome** on the held-out date. Their visit, filmed time and stigmatic CP/HP observations exist in the original source; their fruit Seed.set does not. **No missing value is used for training, and no seed value is imputed**.
4. Compute best- and worst-case potential squared-error difference for each missing flower, *conditional* on a hypothetical comparable `Seed.set` value (y_i\in[0,1]).

The original M0-versus-M1 squared-error difference is

\[
\delta_i(y_i)=(\widehat y_{0i}-y_i)^2-(\widehat y_{1i}-y_i)^2
=\widehat y_{0i}^{2}-\widehat y_{1i}^{2}
+2y_i(\widehat y_{1i}-\widehat y_{0i}).
\]

It is affine in the unobserved (y_i), so for the **fixed predictions** the extrema over all 29 unobserved values are exactly the sums of the individual extremes at `y=0` and `y=1`, without any assumption that fruit loss is missing at random. It is mathematically sharp when each missing latent response can vary independently on [0,1]. This is **not** a confidence interval or an estimate of the missing values.

## Original-source numerical result

| Original cohort | Known value or possible squared-error gain M0−M1 |
|---|---:|
| Recovered 93 flowers: fixed original pooled MSE gain | **+0.001314485** |
| Recovered 93 flowers: sum of squared-error gains | +0.12224706 |
| Unrecovered 29 flowers: **minimum possible total** squared-error gain | **−1.15006075** |
| Unrecovered 29 flowers: **maximum possible total** squared-error gain | **+1.16036146** |
| **All 122 flowers: lowest possible fixed-forecast pooled MSE gain** | **−0.00842470** |
| **All 122 flowers: highest possible fixed-forecast pooled MSE gain** | **+0.01051318** |

A positive difference means M1 (visit+measured pollen) would have smaller held-out MSE; a negative one means M0 (visit without pollen) would be better. **Both directions remain possible** once the original 29 unrecovered fruits are acknowledged; the 93-fruit gain cannot establish which model would predict hypothetical outcomes for all filmed flowers better.

The missing 29 outcomes are concentrated at:
- Day 176: **15**, potential missing-outcome total squared-error gain **[−0.65454, +0.71128]**.
- Day 178: **8**, **[−0.27133, +0.23245]**.
- Days 182, 183, 190, 196: **2, 1, 2, 1** respectively.

These ranges were computed using one fixed out-of-date prediction per unrecovered flower, but only **date-level counts/means and bounds** are stored publicly, never per-flower visits, stigma grain counts, seed data or field identifiers. An independent artifact_tool original-XLSX import with NumPy ridge revalidated the original **32/32 source fold metrics to a maximum absolute error of ~1.11×10^-16**; the accompanying pure-stdlib source-locked script reproduces the same setup and aggregates.

## Ecological interpretation and identification limit

The observed 93-fruit result already failed its two-part prospective success criterion. The new post-outcome mathematics now demonstrates a *further* limitation: **even the sign of the full original 122-flower fixed-forecast error comparison is unidentified without outcomes for the 29 unrecovered flowers**. This is a precise outcome-ascertainment problem, not a demonstration that CP/HP pollen quantity has no biological effect or that pollen transfer is universally a bad predictor.

**Most important caveat:** a flower whose mature fruit was consumed or lost may not have a biologically meaningful latent *source-comparable* `Seed.set` at all. In that case, this all-122 hypothetical target is itself an **estimand definition problem**, and even the mathematical interval does not represent a field-realized function. The interval is conditional on defining a potential 0–1 comparable seed maturation fraction for every flower.

The interval is also a bound on the scores of the **models trained on the original recovered 93 fruit outcomes**, not on predictions a model might have made if all 122 fruit outcomes had actually been collected and used in training. Do not confuse it with new cross-validated risk of a hypothetical all-complete 122-flower dataset.

**Source-aware future natural monitoring design:** record the observation *and transition process* on the same focal flower and mother: filmed visits, CP/HP deposition, compatible paternal source (where feasible), abortive/immature seed counts, fruit predation/removal, mature-fruit recovery, seed output and viable recruitment across dates and in **independent populations**. Predefine a functional endpoint that exists for fruit losses; distinguish failure of function from lack of observation, and stratify forecast calibration across early/late phenology.

All original LA005/CY002, QPF001 preregistered null, source-atlas QPF denominator, EGWEE synthesis and theoretical EGWE findings are unchanged. This is a rigorous limit on the *measurement-to-function translation* of this particular study, not identification of universal functional fragmentation.

## Reproducibility and privacy boundary

```bash
python research/qpf_public_source_recovery/bound_qpf001_missing29_fixed_forecasts.py \
  --source-zip /private/path/doi_10_5061_dryad_hqbzkh1g9__v20210608.zip \
  --output /tmp/qpf001_missing29_bounds_private_audit.json
```

The script validates the original source SHA256/CRC and original protocol commit ancestry, exactly reproduces all registered 8-day MSE/MAE results, and writes only date-level/model-level aggregates and conditional bounds. No third-party original XLSX, ZIP, flower identities, pollen/seed observations or unknown-response guesses are committed; GitHub CI checks the code and archived bounds using synthetic examples but cannot reopen the user's original private source.
