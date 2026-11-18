# QPF001 — flower-level stigma pollen does not reliably improve held-out-date seed-set prediction

**Executed 2026-11-18. Fixed decision: `NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN`.** This is a **reanalysis of an original 2021 one-site field dataset**, not a new field experiment, external independent landscape confirmation, causal mechanism identification or a universal functional-fragmentation principle.

## Exact original source / temporal registration

Smith, Swartz & Spigler (2021), *American Journal of Botany* 108:1612–1624, [DOI 10.1002/ajb2.1720](https://doi.org/10.1002/ajb2.1720), original Dryad source [10.5061/dryad.hqbzkh1g9](https://doi.org/10.5061/dryad.hqbzkh1g9).

The user provided the exact **2021-06-08** Dryad ZIP `doi_10_5061_dryad_hqbzkh1g9__v20210608.zip` (archive SHA256 `09a47a94913c7087405679c5dc18c0c3c6ded4e8ecad298e6f94f87c5a78b653`). The only inner source, `FIGO_2019_Data_20210523.xlsx`, is **27,351 bytes** and SHA256 `83790bb7d63222e3e21c0ceed5d729cacf63a2df843e5807836d8e5c853447aa`, exactly the independent official Dryad manifest. Both outer/inner ZIP CRC checks passed. Neither original ZIP, workbook nor any flower-level values are committed to this repository.

Before examining seed/pollen/visitation response associations, the source names, cell types and denominators were inspected and the **frozen scientific model protocol** committed alone as `a1658c353a0c244edafab194f96301968dc84040` (`QPF001_FROZEN_DATE_POLLEN_SEED_PROTOCOL_20261118.json`). Every subsequent result is interpreted under that fixed design, with no post-hoc response substitutions, selected filming dates or feature/penalty search.

## Biological grain and source completeness

The original 12-ha Pennsylvania grassland study tagged **122 distinct maternal plants** and observed **one focal flower per plant** during 2019. Each focal flower's original Excel record contains filming date, filming duration, legitimate contacts by four bee/fly functional groups, surrounding conspecific/heterospecific floral abundance, next-day same-flower stigmatic **conspecific pollen (CP)** and **heterospecific pollen (HP)** counts, and a mature-fruit seed-set result where recovered. The parent paper **already discovered** a seed-set cost of HP that was modified by CP deposition, so this relationship is prior art, *not* an EGWEE new biological finding.

| Original measured unit | Verified count |
|---|---:|
| Unique filmed flowers / mother plants | **122** |
| Unique filming days (Julian day 176, 177, 178, 182, 183, 190, 191, 196) | **8** |
| Source contact-visit and CP/HP stigma deposition data | **122 flowers** |
| Recovered fruit / numerical original `Seed.set` | **93 flowers** |
| Unrecovered fruit / literal `NA` seed outcome | **29 flowers** |
| Missing conspecific and heterospecific neighborhood fields | **6 flowers**, including **5** of the 93 with seed set |
| Seed-complete flowers by 8 original filming dates | **16, 18, 18, 18, 7, 4, 8, 4** |

29 unrecovered/possibly herbivorized fruit outcomes are **missing**, not zero biological seed set. No outcome-missing-at-random assumption is validated by the dataset. The 5 seed-complete flowers missing floral-context counts are **retained** and imputed using only each training fold's median of log neighborhood abundance, with two explicit missingness indicators. **Day 196's four seed-complete observations all lack neighborhood values** and are retained, never selectively dropped.

## Frozen Q versus Q+P predictive estimand

- **Response F:** original source `Seed.set` (0–1), not imputed for 29 missing mature fruits; MSE and MAE per recovered flower.
- **Baseline Q model M0:** source Julian day, two log(1+floral neighbor count) terms + missingness indicators, four log(1+legitimate visit contacts per film-hour) for large bees, small bees, small flies, large flies.
- **Transfer-augmented M1:** M0 + log(1+CP.Count) + log(1+HP.Count) + their product. The product was specified from **prior published evidence**, not selected using this held-out response.
- **Learning:** training-date-only neighborhood imputation and feature standardization; ridge with λ=1, unpenalized intercept; predictions of both models clipped to [0,1].
- **Validation:** leave an *entire filming Julian day* out, all 8 days (not 93 randomly assigned flower folds); positive result required **≥5% flower-weighted pooled MSE improvement AND ≥6 of 8 positive held-out day folds**. This is a within-study temporal transfer criterion, **not** external system replication. No other outcomes or tuning allowed after results.

## Original complete results

| Held-out Julian day | Scored flowers | M0 MSE | M1 MSE | Improvement M0−M1 |
|---|---:|---:|---:|---:|
| 176 | 16 | 0.075832 | 0.072297 | +0.003534 |
| 177 | 18 | 0.081535 | 0.075286 | +0.006248 |
| 178 | 18 | 0.063255 | 0.058771 | +0.004484 |
| 182 | 18 | 0.038567 | 0.044007 | −0.005440 |
| 183 | 7 | 0.044857 | 0.046303 | −0.001447 |
| 190 | 4 | 0.080069 | 0.115120 | **−0.035050** |
| 191 | 8 | 0.159545 | 0.159941 | −0.000396 |
| 196 | 4 | 0.593169 | 0.562185 | +0.030984 |
| **Pooled recovered flowers** | **93** | **0.094592** | **0.093277** | **+0.001314** |

Overall adding the measured stigma pollen composition **reduced MSE by only 1.39%** and **4 of 8 dates** improved. The predeclared joint criterion (≥5% and 6/8) therefore **fails**. Pooled MAE declined slightly `0.245170 → 0.243044`, not a second alternative success criterion. Two late held-out dates have only four recovered fruit records each, and the day-196 MSE is high; there are too few independent date clusters for reliable universal predictive inference. This does **not** refute the published in-sample HP×CP effect or demonstrate an absence of real pollination mechanisms.

## Important original-variable discrepancy — no response replacement

The original `Metadata` worksheet defines `Seed.set` as a proportion of ovules developing into mature seeds and `Seed.weights` as `Seed.count + Small.seed + Ovule`. In all **93 recovered fruits** source `Seed.set` equals `Seed.count / Seed.weights`. Yet the original paper's textual formula defines mature seeds divided by mature seeds **plus unfertilized ovules**; that alternative formula gives the **same numeric value in 83/93** fruits, not all 93. The difference is confined to **10 source fruits** and appears consistent with whether immature seeds enter the denominator, but this is a source/definition-level reconciliation issue, **not** proof of publication error. The primary response was frozen as source `Seed.set`, so it was **not modified after the negative result**. Interpret comparisons with published seed-set coefficients under this distinction.

## Independent reproduction and claims

The original workbook was imported through **artifact_tool** and fitted by NumPy ridge normal equations. A separately written **standard-library OOXML+Gaussian elimination** parser/regression reproduced **8 dates × 2 models × MSE/MAE = 32 aggregate metrics** with maximum absolute difference **1.55×10⁻¹⁵**. The original source study's HP×CP effect is a known prior result; our additional **heldout-date transport test** does not robustly support a practical predictive gain from stigma CP/HP quantity relative to a visitation+context baseline.

The new result **does not test genetically compatible pollen**, paternal identity, viable recruitment, the EGC–EGWE finite model's allele sorting/repair mechanism, or an island–urban functional-fragmentation convergence law. This source is one grassland and eight calendar-day groups; it adds no independent landscape-level system count to the QPF atlas. Missing mature fruits and unknown sampling mechanisms also preclude a claim about population-wide fertilization failure.

### Source-verified command (no raw third-party data committed)

```bash
python research/qpf_public_source_recovery/run_qpf001_original_flower_dateholdout.py \
 --source-zip /local/private/doi_10_5061_dryad_hqbzkh1g9__v20210608.zip \
 --output /tmp/qpf001_original_8day_aggregate.json
```

Only aggregate source counts and model diagnostics are written; the source archive stays outside GitHub. CI is **source-withheld**, using synthetic regression tests and the committed aggregate receipt; successful CI by itself must not be misdescribed as a full original-file rerun. All prior LA001, LA002 and CY002 negative results and LA005's small within-study marker result remain unchanged.
