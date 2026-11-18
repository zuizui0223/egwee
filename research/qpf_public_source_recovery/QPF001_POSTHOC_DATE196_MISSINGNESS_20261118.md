# QPF001 posthoc event audit: late-date prediction failure and selective fruit recovery

**2026-11-18 — POST-OUTCOME DESCRIPTIVE AUDIT ONLY. The original preregistered result is unchanged:** `NO_ROBUST_WITHIN_STUDY_DATE_TRANSFER_GAIN`.

The source is the original user-supplied *Oenothera fruticosa* 2021 Dryad archive [10.5061/dryad.hqbzkh1g9](https://doi.org/10.5061/dryad.hqbzkh1g9), ZIP SHA256 `09a47a94913c7087405679c5dc18c0c3c6ded4e8ecad298e6f94f87c5a78b653`, original XLSX SHA256 `83790bb7d63222e3e21c0ceed5d729cacf63a2df843e5807836d8e5c853447aa`. Original locked scientific protocol `a1658c353a0c244edafab194f96301968dc84040`, original [result](QPF001_ORIGINAL_DATE_HOLDOUT_RESULT_20261118.md) and [eight-date JSON](QPF001_DATE_HOLDOUT_ORIGINAL_RESULT_20261118.json). No parameters or registered outcome were changed.

## Original predictive improvement: almost entirely one late day

The frozen 93-fruit date-heldout pollen-augmented model M1 reduced aggregate MSE over visit/context baseline M0 from **0.094592 to 0.093277**, a **+0.001314** M0–M1 gain, only **4/8 positive dates**; the prespecified **5% and ≥6/8** improvement gate **failed**.

Exactly decomposing the **already stored**, original eight date-loss contributions yields:

| Original date-loss quantity | M0−M1 |
|---|---:|
| Original pooled gain, 93 recovered flowers | **+0.001314485** |
| Julian day 196's contribution to that 93-flower gain | **+0.001332645** |
| Other seven dates, 89 previously scored flowers, *original predictions with no model refitting* | **−0.000018977** |

The apparent positive pooled MSE gain is **entirely accounted for by day 196's four recovered flowers**. This is a *descriptive algebraic decomposition*, **NOT** a registered leave-one-day-196-out sensitivity analysis, not a new 89-flower result and not permission to delete this date and claim negative biological association.

## Why late day 196 is hard to predict

| Original filming day | Filmed flowers | Recovered fruits | Unrecovered outcomes | Mean recorded source Seed.set | M0 mean forecast | M1 mean forecast |
|---|---:|---:|---:|---:|---:|---:|
| 176 | 31 | 16 | 15 | 0.5120 | 0.4232 | 0.4399 |
| 177 | 18 | 18 | 0 | 0.3745 | 0.4989 | 0.4827 |
| 178 | 26 | 18 | 8 | 0.4224 | 0.4354 | 0.4409 |
| 182 | 20 | 18 | 2 | 0.3974 | 0.3942 | 0.3899 |
| 183 | 8 | 7 | 1 | 0.4913 | 0.3590 | 0.3742 |
| 190 | 6 | 4 | 2 | 0.1978 | 0.3080 | 0.2868 |
| 191 | 8 | 8 | 0 | 0.3837 | 0.2697 | 0.2605 |
| **196** | **5** | **4** | **1** | **0.0050** | **0.7740** | **0.7531** |

All four **recovered** day-196 flowers lacked both source floral-neighborhood variables; its one unrecovered flower also lacked neighborhood counts, so **all five filmed day-196 flowers** had missing neighborhood information. The fixed prediction model imputed those counts from **training dates only** and used a linearly standardized Julian day value. Day 196 is **later than every training date** when held out; time is being extrapolated. With M0 predicting ~0.774 versus true mean source seed-set ~0.005, and M1 still ~0.753, **neither model identifies the late-season collapse**. It is not just a failure of *pollen abundance* alone.

A source-support check against other dates' training log1p(CP/HP) 5th–95th percentiles showed **0/4 day-196 CP values above CP p95, 1/4 below CP p05; 0/4 HP values outside either endpoint**. This argues against a simple story that all four late flowers had unprecedented high/low pollen count; it does **not** identify ecological resource limitation, seasonal regulation, differential fertilization or fruit attrition. All are candidate explanations only.

## Outcome ascertainment is highly heterogeneous by filming date

The original study filmed **122 flowers** and successfully recovered mature-fruit `Seed.set` for **93**; the remaining **29 (23.8%)** have **missing outcomes**, **not observed zeros**. Of those 29, **23** are concentrated in just days **176 and 178**, i.e. 15/31 and 8/26 filmed flowers, respectively. Both 177 and 191 have 100% fruit response ascertainment.

The source still contains visit and stigmatic CP/HP measurements for unrecovered flowers. Pooling *only for descriptive upstream-measurement comparison*:

| Original source grouping | Recovered (n=93) | Unrecovered (n=29) |
|---|---:|---:|
| Mean CP grains on stigma | **794.85** | **1,578.76** |
| Mean HP grains on stigma | 326.38 | 260.10 |
| Mean legitimate visitor contacts per filmed hour | **2.658** | **1.185** |

Those differences indicate that the analysed fruit-recovered set **does not have identical recorded covariate distributions to the missing-outcome set**. They are **confounded by filming date** and give neither a reason for fruit loss nor a reliable missing-at-random model. The unrecovered fruits' seed-set values remain unknown.

### A transparent partial-identification limit — no imputation

Among 93 recovered fruits, the source `Seed.set` sum is **37.00813**, mean **0.39794**. If one **hypothetically** defines a comparable latent seed-set proportion (bounded 0–1) for **each of the 29 unrecovered flowers**, without assuming any missingness model, then the mean over **all 122 filmed flowers** is only set-identified in

**[0.30335, 0.54105]** (width 0.23770).

This is **not an estimate of realized seed recruitment or ecological function for lost/herbivorized fruits**. It is an arithmetic best/worst-case illustration of what the unobserved values prevent one from inferring. No unrecovered fruit was coded as zero in the frozen QPF001 predictive comparison.

## Original seed-set source definition remains a separate issue

The original `Seed.set` equals `Seed.count / Seed.weights` in **93/93** recovered fruits, but equals the source paper text's `Seed.count/(Seed.count + Ovule)` expression in only **83/93**. Ten differ (by date: 176:1, 177:4, 178:1, 182:1, 183:2, 191:1). The original registered response is retained. This measurement discrepancy and missingness are distinct limitations, not instructions to posthoc select favorable definitions.

## Ecological interpretation, identification ceiling and replication

A defensible bounded conclusion is:

> In this source, a nearly-zero late-season seed-set group, with incomplete floral context and Julian-date extrapolation, overwhelmingly determines the small apparent positive pooled predictive gain from adding CP/HP pollen counts. The remaining 29 unrecovered fruits also select the observed model sample nonuniformly across dates and upstream CP/visit measurements. Therefore the failure to achieve a stable within-study date-transfer gain cannot be attributed to one pollen mechanism or interpreted as a universal Q→P→F invariance.

The original article [Smith et al. 2021](https://doi.org/10.1002/ajb2.1720) already published the pollen composition × seed-set relationship. This posthoc audit supplies an **operational failure mode of our own predictor transport attempt**, not a new causal discovery or a reassessment of the paper. One grassland, eight filming dates, and no genetically compatible pollen/paternity or offspring recruitment cannot support cross-fragmentation convergence.

**Next independent-system design:** record `I` visits and observation effort; `P` stigma CP/HP and genetically compatible donor provenance if available; `F` seeds and viable recruitment; **`M` seasonal cohort/time and fruit recovery/attrition status**, all on the same mother×flower×date. Freeze a pre-outcome time-block holdout with adequate late-season response and observed neighborhood environment. An unmeasured recovery/maturation process cannot be treated as fixed zero, and cross-programme results must hold out independent biological studies, not merely dates.

## Reproducibility

`diagnose_qpf001_date196_missingness.py` reopens the exact original private ZIP, verifies its SHA, CRC and the original protocol's immutable Git ancestry, regenerates the original 8×2 frozen predictions, matches their archived MSE and MAE, and outputs **only source-aggregated date/completeness/pollen/visitation summaries**. CI excludes the original third-party ZIP and only checks the source-withheld audit code and aggregate receipt. All original QPF001 and LA001/LA002/LA005/CY002 outcomes remain frozen.
