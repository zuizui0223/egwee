# Corrected EuPPollNet post-primary source-backed robustness: calendar-day and shared-host guild floral-use
**Date: 2026-11-18. Status: retrospective exploratory sensitivities following registered main result.**

The hypotheses and threshold rules for these two sensitivity analyses were fixed in \`POSTPRIMARY_ROBUSTNESS_FREEZE_20261118.md\` only **after the positive primary 311-network/39-programme result was observed**. They are NOT additional outcome-blind preregistrations and should never be counted as two independent confirmations. Original source author repo \`joseblanuza/EuPPollNet@31716d21d5aad8c27c1d91dd0620149ef42e8836\`; corrected source \`Interaction_data.csv.gz\` SHA256 \`6e4e5399338d530462d8683b53a5e564d48e287e423be420c07d8046815ef38a\`, 623,476 original interaction rows.

## Reproduced exploratory outcomes

Final [GitHub Actions run 44224413979](https://github.com/zuizui0223/egwee/actions/runs/44224413979) was **SUCCESS**, including original source integrity, preregistered main result reproduction, self-tests of date parser/shared-host inclusion and retrospective robustness estimator. Original data rows were not redistributed. Each sensitivity uses 199 within-unit multivariate-hypergeometric guild-label shuffles to correct the observed Jensen–Shannon divergence for finite insect records and observed pooled plant-use distribution. Report equal independent-original-programme means and 2,000 whole-programme bootstrap resamples, rather than counting nested network/date units as independent programmes.

| Source-defined robustness unit | Eligible nested units | Eligible independent original programmes | Programme means positive | Equal-programme excess JSD (nats) | Whole-programme 95% CI |
|---|---:|---:|---:|---:|---:|
| Study × network × exact calendar date (>=10 wild-bee, >=10 syrphid visits, >=3 plants on that date) | **569** | **42** | **42 / 42** | **+0.19918200** | **[+0.17585904, +0.22336082]** |
| Study × network × year **restricted to plant taxa actually visited by both focal guilds** (>=3 shared plant taxa, >=20 focal visits in each guild after restriction) | **217** | **33** | **31 / 33** | **+0.11835500** | **[+0.09336263, +0.14482448]** |

Source has **6,203** date-group source units and 1,864 study×network×year units overall. Calendar-day model excludes 5,634 date units for preregistered post-primary coverage. Shared-host model excludes 1,647 source network-year units. Missing/undercovered source units remain non-comparable, not evidence of biological absence.

## Interpretation and inferential limits

The original 311-network/39-study study-equal **+0.23232269 nats** observed floral-use separation remains the only preregistered primary estimand. This additional result suggests a portion of guild-specific plant-use allocation persists when comparisons are restricted to coincident **survey date** and when total host-list differences are partly removed by analyzing **plant taxa used by both guilds**. Crucially, even the latter does *not* condition on same-day visitation at the same site, same local blooms, independent flower availability or floral abundance. Same-day units do not imply identical observation hours, microhabitats or true flower supply. The two sensitivities use different inclusion criteria and cannot be interpreted as a fixed-fraction decomposition of the original +0.232 value.

The conclusion is specific and positive: guild identity carries information about **which plants are visited** beyond finite-sample differences and pooled observed visitation, both in pooled networks and in the narrowed observed subsets. It does **not** establish causal preference, competition, niche separation against independent flower-supply composition, compatible pollen transfer, seed set, reproductive success, or any fragmentation treatment effect. Differences between survey programmes and potential observer/bloom-hour biases remain. Strong wild-bee/hoverfly floral-use differences themselves are not conceptually unprecedented: a journal novelty claim needs comparison with prior guild-partition studies and careful evidence on external generality.

## Decision

Retain as well-supported **observation-network macroecology** and a candidate for an independent empirical paper section, with study nesting and source correction explicit. Next scientifically decisive tests, if a separately registered new analysis is designed, would combine network observations with directly measured co-sampled plant flower availability (\`Flower_counts.csv\` with 199,692 records, original unit/codebook verification required) and ideally independent study-matched seed-function data. Neither is silently inferred in this analysis. Preserve draft status: this is not yet evidence for a general ecological function/fragmentation law or theoretical \`egwe\`.
