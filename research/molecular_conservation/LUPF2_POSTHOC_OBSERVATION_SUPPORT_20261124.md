# LUPF2 posthoc observation-support audit — source strata, not a new result

**2026-11-24.** Executed on source Figshare `10.6084/m9.figshare.29606180.v1`, original workbook SHA256 `7d0c86d290cf93968cf4f1b155a4ca1647ee399520d9b5ada66f74e892235734`. GitHub Actions [run 45329193843](https://github.com/zuizui0223/egwee/actions/runs/45329193843) completed with original source-only [artifact 14890738390](https://github.com/zuizui0223/egwee/actions/runs/45329193843/artifacts/14890738390), ZIP SHA256 `2f1d5e74fba6fc8652f7d673cde84bf74ff02a5cf767e608bdb111fa5faf464a`. **No regression, outcome direction, effect size or new model estimated.** Positive exploratory LUPF2 signed result from [run 45328763380](https://github.com/zuizui0223/egwee/actions/runs/45328763380) remains immutable and is not rerun in subsequent workflow commits.

## Complete source denominators by original anonymous code

Original source design had 3,024 records and source-coded `population` FRO/PIC plus `line` C/J/L/R/T/X. `line` codes have **no verified intervention mapping** (not control vs assisted gene flow). Grouping `genotype` are source labels, **not measured SNP genotypes**.

| Source population | Source code | Total rows | Both seed numeric and onset numeric | Joint completeness |
|---|---|---:|---:|---:|
| FRO | C | 360 | 247 | 68.6% |
| FRO | J | 288 | 206 | 71.5% |
| FRO | L | 360 | 246 | 68.3% |
| FRO | R | 144 | 97 | 67.4% |
| FRO | T | 360 | 253 | 70.3% |
| FRO | X | 72 | 53 | 73.6% |
| PIC | C | 360 | 218 | 60.6% |
| PIC | J | 360 | 249 | 69.2% |
| PIC | L | 360 | 219 | 60.8% |
| PIC | T | 360 | 220 | 61.1% |
| **FRO total** | **six codes** | **1,584** | **1,102** | **69.6%** |
| **PIC total** | **four codes** | **1,440** | **906** | **62.9%** |
| **Overall** | **10 original pop×line cells** | **3,024** | **2,008** | **66.4%** |

Nonrandom observation is plausible: jointly missing 956 records, seed-only missing 34, onset-only missing 26. A source `number of seeds` zero was **not** imputed for missing cases. R/X appear **only in FRO**, which prevents treating all source line types as replicated contrasts across both populations. The source has only two founding northern population locations; 2,008 records and 84 genotype groups do not constitute 2,008 independent natural populations.

## Consequences for the earlier exploratory positive result

`LUPF2_EXPLORATORY_HOLDOUT_RESULT_20261124.md` showed MSE 1.134807 baseline versus 0.870675 + flowering onset, gain +0.264132, 5/5 genotype-group held-out fold wins, **within the 2,008 complete cases**. This result is not invalidated arithmetically by the source strata. However, it is **conditional on selection into observation**; differential completeness FRO/PIC and C/J/L/R/T/X, possibly ecological mortality / nonflowering, could change inference for all originally sown individuals. One must not identify missing seed index with plant death or zero seed output without experimental records. The interval in the exploratory result does not handle MNAR selection, environmental between-population transfer, or model refitting uncertainty.

**No respecification, treatment recoding, subset selection or additional fit** was attempted based on the support audit. To extend the biological inference requires verified line-code interpretation, cohort/plant survival outcomes and an independent seed/viable recruit series with effective pollen measures, and likely a separate prospective protocol. Original preregistered strict LUPF1 remains stopped.
