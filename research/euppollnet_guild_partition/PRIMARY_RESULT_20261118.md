# EuPPollNet corrected 2025 source: wild bee–hoverfly floral-use partition (2026-11-18)

## Status: first source-verified positive macroecological observation result

Empirical \`egwee\`, independent of theoretical \`egwe\`, PoMS FIT/pan channel comparisons, the five-cluster Hedges-g fragmentation meta, Leavenworthia genotype assays and direct plant seed function. This is an **observed floral-use / interaction allocation** result, not causal competition, pollen deposition or wild plant seed-setting.

### Pre-outcome witnesses

- Initial biological hypothesis, exact network/guild thresholds, Shannon/Jensen–Shannon estimator, 199 finite-sample hypergeometric nulls, 2,000 whole-programme bootstraps and claim rule were frozen in \`PROTOCOL_20261118.md\` **before opening numeric guild-use associations** (commit \`bb9b3607\`).
- Original author repository \`joseblanuza/EuPPollNet@31716d21d5aad8c27c1d91dd0620149ef42e8836\`; original corrected \`Interaction_data.csv.gz\` SHA256 \`6e4e5399338d530462d8683b53a5e564d48e287e423be420c07d8046815ef38a\`.
- The published correction \`10.1111/geb.70054\` fixes interaction duplication and points to Zenodo \`10.5281/zenodo.15183272\`. **623,476** interactions are correct; the original 1,162,109 count must not be used.
- Source schema and original IDs were separately checked before effect estimation, in \`SOURCE_ID_GATE_RESULT_20261118.md\`. **623,476 rows / 1,864 source networks / 54 nominal study IDs / 52 independent original study programmes**. \`Interaction\` records verified as original unit records. All guild and plant IDs are source taxonomic fields, not inferred from proximity.
- Final result **CI SUCCESS**: [run 44223677770](https://github.com/zuizui0223/egwee/actions/runs/44223677770), with original source download SHA verification, synthetic hypergeometric/JSD identity test, source coverage and derivative-only upload. No original source visitor rows redistributed.

### Confirmatory registered partition estimator

The eligibility condition (at least **20 wild bee and 20 syrphid records plus 3 plant taxa** within one original method/site-year network) retained **311 networks from 39 of 52 original study programmes**, excluding 1,553 network keys for insufficient coverage. The main effect per network is the observed wild-bee vs syrphid Jensen–Shannon divergence of plant-use proportions minus its mean expectation from 199 guild-label permutations conditioning on the observed pooled plant counts and both guild total visit counts.

| Registered primary quantity | Source-verified result |
|---|---:|
| Original source network keys | 1,864 |
| Eligible networks | **311** |
| Independent original study programmes with eligible networks | **39** |
| Study programmes with positive mean excess partition | **39/39** |
| Equal-programme mean excess JSD (nats) | **+0.23232269** |
| 95% whole-programme bootstrap percentile CI (2,000 draws) | **[+0.20928882, +0.25395883]** |
| Leave-one-programme-out mean range | **[+0.22815680, +0.23660419]** |
| Fixed directional support rule | **PASS** (CI excludes 0 and >=70% programmes positive) |
| Secondary equal-network mean excess | +0.23198971 |
| Mean raw observed JSD, equal networks | 0.32003165 |
| Mean 199-null expected JSD, equal networks | 0.08804193 |

Eligible networks per source programme: min 1, median 4, max 47; bootstrap independently resamples whole programme *means*, not individual visits, species or networks.

### Secondary source observation methods (no independent method hypothesis)

| Source method | Eligible networks | Descriptive mean excess JSD |
|---|---:|---:|
| Focal observation | 93 | +0.25983 |
| Plot | 17 | +0.17790 |
| Random walk | 6 | +0.28795 |
| Random census | 6 | +0.18236 |
| Transect | 183 | +0.22454 |
| Transect/Random walk | 6 | +0.17457 |

These method means are descriptive, studies/methods confounded. **No method-specific causal sampling effect** is inferred.

### Mechanistic and novelty boundary

The result is a reproducible cross-programme *magnitude* for observed guild-specific use of flowering-plant taxa beyond finite samples and observed pooled visit frequencies. Ecologically it shows that local visitation allocation is guild dependent; it challenges using an undifferentiated pollinator visit count as a sufficient descriptor of interactions.

However, partitioning in pooled site-year networks might be influenced by **different seasonal flights, host plant phenology, sampling dates or taxon resolution**, not contemporaneous guild-specific preference. The randomization preserves plant-use totals *over the network time-window*, not measured independent flower availability. Strong guild partition itself is already well known; the novelty must come from robust cross-study quantification **and** additional same-date/resource-supply validation. It does **not** measure effective pollen transfer, compatible seed set, genetic diversity or how fragmentation affects reproductive function.

The source \`Flower_counts.csv\` has 199,692 records, but units of flower measurement vary across studies, so it is not silently treated as a uniform abundance denominator. Post-primary date-concurrent and shared-plant tests, if run, must be clearly identified as retrospective sensitivity, not another preregistered success criterion.

**Publication readiness: exploratory evidence package, not a finished functional-ecology or fragmentation paper.**
