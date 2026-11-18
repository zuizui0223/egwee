# Post-result CropPol audit: no-visit baseline and field-fold stability

Date: 2026-11-18. **Post-outcome exploratory diagnostic** (the original M0 vs M1 20-programme result has already been computed). This is not a new unexposed confirmation and must not change the primary frozen decision `NO_RESOLVED_STUDY_GENERAL_GUILD_COMPOSITION_INCREMENT`.

## Why this distinct diagnostic is needed

The frozen 20-programme, 29-panel, 591-field result showed mean M0−M1 MSE gain **−0.44720563**, with 4/20 positive programme means and 95% source-programme bootstrap `[-1.23535,-0.00723]`. Adding one predictor may harm small sample cross-validation through estimation noise. To understand the observational *predictive* rather than causal meaning, test whether total visits offer any information over the training-only mean and whether the negative incremental sign persists across fixed alternative field splits.

## Exact rules before diagnostic execution

1. **Same original source and sample**, no extra filters, crops, guilds, outcome transforms, zero-field rescues, excluded panels, panel weights or altered ridge penalty. 29 eligible panels, 20 original study programmes, 591 independent fields must match previously pinned source exact Git blob.
2. **Mnull**: for each held-out field fold, predict **training-only mean log1p(yield)**, scored as zero against test train-standardized outcomes. Compare Mnull vs existing M0 (total-source-visit feature) under exactly the **original hash 5-fold** assignment; preserve baseline same sample and training scaling. M0 positive gain means total visits improve vs constant predictor, but no causal influence.
3. **50 alternative fivefold field splits**, deterministic SHA256(key `seed=0,...,49` × exact source field key) % 5, same fold assignment for M0 and M1. The models remain training-only ridge lambda=1, same factors and training-only target standardization. Any nonestimable panel is counted and yields an explicit STOP for that seed; no selecting favorable seeds. For each complete seed, average panel gains within study group and then average study means; report all-seed aggregate min/median/max, 10th/90th percentiles, number of positive seeds. These are **split-sensitivity descriptions, not independent biological replications or confidence intervals**.
4. Keep original selected 20-programme benchmark fixed and report the Mnull−M0 study-equal mean plus 2000 whole-programme bootstrap percentile interval (seed `20261128`) as **post-primary** context, not a substitute primary.
5. If any source checksum / 29/20/591 sample count / overlap / trait definition drifts, STOP. Original outcome and individual field-level records must not be redistributed. Permutation of variables or threshold tuning is **not** included because both are additional after-outcome models and cannot rescue a prespecified failure.

Interpretation: even if the source visit total or guild composition loses predictive power with these field splits, the result does **not** reject real pollination, since crop production has other determinants and the missing compatible-pollen and flower-hour variables are unchanged. A range of field-split effects remains within the same non-independent CropPol original corpus. The original absolute effect and main PR #72 EuPPollNet result are not revised.
