# Protocol amendment — multilayer clusters and within-cluster covariance

**Locked:** 2026-09-12, before any cross-system multilayer synthesis.

This amendment tightens the dependence rules in `META_ANALYSIS_PROTOCOL_2026-09-11.md`. It does not change the biological layers, effect orientation, or the effect-unit firewall. It prevents one multilayer study from being counted as several independent studies and defines when a set of effects can contribute a paired cross-layer contrast.

## 1. Primary synthesis unit

The primary cross-system denominator is a **multilayer cluster**, not an extracted effect row.

A cluster is identified by the joint identity of:

`study/species x source-defined fragmentation contrast x campaign/observation window x independent-unit frame`.

Multiple endpoints or layers measured on the same units under the same contrast remain separate effect rows inside one cluster. They do not increase the number of independent studies or clusters.

## 2. Multilayer-cluster admission contract

A cluster is eligible for a paired cross-layer synthesis only when all of the following hold:

1. at least two predeclared biological layers have admissible quantitative effects;
2. the fragmentation exposure/contrast is the same source-defined exposure for those layers and was defined independently of their outcomes;
3. the independent-unit frame is shared or its overlap/nesting can be explicitly reconstructed;
4. campaign/year/cohort differences are represented explicitly and are not silently concatenated into one synchronized observation;
5. alternate representations of the same observation (for example `H_O` versus `F_IS`, or `r_p` versus `N_ep=1/r_p`) are marked as sensitivity/duplicate representations rather than extra independent outcomes;
6. within-cluster sampling dependence is represented by a covariance block when reconstructable, or by the declared cluster-robust fallback when it is not.

A study may therefore be multilayer in biological content but still be `candidate` rather than `admissible_multilayer_cluster` until its effect-unit and dependence contract is satisfied.

## 3. Covariance hierarchy

Within-cluster covariance is handled in the following order.

### A. Paired independent-unit data available

When the same independent units contribute paired endpoint values, retain the paired unit table. Use the observed within-contrast residual outcome correlation matrix as a transparent proxy for the correlation among sampling errors and combine it with the already-audited marginal sampling variances to construct a working `V` block:

`V_ij = r_ij * sqrt(v_i * v_j)`.

This is an **approximate reconstructed sampling-covariance block**, not an exact known covariance. The unit-level correlation matrix, the resulting `V` block, positive-definiteness check and method label must be stored.

### B. Exact shared-control / source-model covariance available

If the publication or raw-data reanalysis supplies an exact or model-based sampling covariance, prefer that covariance over the proxy in A and record its provenance.

### C. Dependence known but covariance not reconstructable

Do not set covariance to zero. Keep the effects in the same cluster and use study/species/contrast clustering with robust variance estimation in the cross-system model. A rho-sensitivity analysis may be used, but it cannot turn one cluster into multiple independent observations.

## 4. Canonical standardized-effect variance

All binary/contrast effects admitted to the Hedges-g stream use one sampling-variance convention. The canonical definition is the large-sample variance used by `metafor::escalc(measure="SMD", vtype="LS")`:

`V(g) = 1/n_fragmented + 1/n_reference + g^2 / [2(n_fragmented + n_reference)]`.

The small-sample correction is applied to the standardized mean difference to obtain Hedges `g`; the variance formula above is then applied to `g`. Alternative formulas such as `g^2/(2*df)` or `J^2 Var(d)` are not mixed inside the same synthesis. Existing PS003/PS004 effect rows and covariance blocks are harmonised to this convention before any cross-system fit.

## 5. Serapias reference implementation

`PS003` (*Serapias lingua*) is the first reference cluster.

The source-defined anthropic populations `C/F/G` and natural populations `A/B/D/E/H/I` are the same contrast for:

- `C`: pollen immigration rate;
- `F`: fruit set;
- `G_adult`: observed heterozygosity.

All three primary effects use the same nine population units. They are therefore **one cluster with three correlated outcomes**, not three studies. `F_IS` is an alternative adult-genetic sensitivity representation and cannot be added as a fourth independent primary outcome.

The paired site table permits an approximate covariance block to be reconstructed. Because the fragmented group contains only three populations, the empirical correlations are themselves uncertain; this block is retained with an explicit proxy label and must be checked against cluster-robust/rho-sensitivity results once independent clusters accumulate.

## 6. Brosimum second-cluster implementation

`PS004` (*Brosimum alicastrum*) is the second independent admissible cluster.

The source study uses the same three continuous and three fragmented populations for the landscape contrast. The cluster currently admits:

- `C`: site-level multilocus correlated paternity `r_p`, oriented so higher biological support corresponds to lower `r_p`;
- `F`: one-year total plant dry mass (`TPDW`) recovered from the public Figshare workbook by first averaging offspring within maternal tree and then maternal-tree means within population.

The three populations per habitat, not maternal trees or offspring, are the independent fragmentation units. `TPDW` was fixed in the recovery script before its effect values were observed as the primary integrated one-year progeny-vigour endpoint. The paired six-site table supplies the working C-F covariance proxy.

Raw adult and progeny genotypes are also present in the workbook, but `G_adult`/`G_offspring` are **not promoted** yet because the current reconstruction does not exactly reproduce the publication-level Table 2 genetic summaries. They remain a separate raw-QA task and are not needed to admit the C-F cluster.

## 7. Cross-programme temporal rule

A programme containing multiple papers or years is not automatically one multilayer cluster. Publications can share `system_id`/`program_id` while retaining distinct cluster IDs when campaign/window or observation cohorts differ.

In particular, the 2019/2020/2021/2026 *Conospermum undulatum* programme is valuable lag architecture but cannot be concatenated into one contemporaneous I/C/F/G observation. Each campaign must satisfy the cluster contract on its own; programme-level temporal comparisons are a separate analysis.

## 8. Current candidate classification

- `PS003 Serapias`: **admissible multilayer cluster** (`C/F/G_adult`), covariance proxy reconstructable from the paired nine-population table.
- `PS004 Brosimum`: **admissible multilayer cluster** (`C/F`), covariance proxy reconstructable from the six paired populations; `G` remains raw-QA pending.
- `PS001 Spondias`: **recoverable but blocked on effect-unit reconstruction**. The biological layers are unusually complete, but lower-level tree/offspring/locus denominators cannot be promoted to site-level replication.
- `PS015 Conospermum 2020`: **gradient candidate** for `I/F` once source coefficients/SE or raw population data under one declared fragmentation predictor are recovered.
- `PS011 Conospermum 2026`: **gradient candidate** for `C/G_offspring`; raw parentage/genotype data can support a population-aware reanalysis, while the standing adult cohort remains a linked historical context rather than a duplicate 2026 effect.
- `PS016 Primula`: **not currently a same-exposure cluster**. Existing reported paths use population size, floral-morph balance, pollinator abundance and nonlinear forest cover as different predictors. A common source-defined landscape exposure must be reconstructed before any G/I/F rows are treated as one fragmentation cluster.

## 9. Gate for cross-system claims

One admissible multilayer cluster can demonstrate that multilayer concordance/state separation is measurable in one system. It cannot establish a cross-system pattern.

No cross-system paired layer conclusion is authorised until at least two independent admissible multilayer clusters satisfy this contract. `PS003` and `PS004` now satisfy that minimum **comparison gate**, so a first cross-system C-F comparison may be run. Passing this gate authorises analysis, not a biological generalisation: with only two clusters, any pooled or concordance conclusion remains explicitly pilot/diagnostic and must be expanded with additional independent systems before a broad cross-system claim.

## 10. Firewall

This amendment is outcome-blind with respect to future candidate admission. A candidate cannot be admitted because its effect directions agree with `PS003`. Admission depends only on the exposure, independent-unit, quantitative-effect and covariance/dependence rules above.