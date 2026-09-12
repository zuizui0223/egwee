# EGWEE multilayer meta-analysis — cluster-first status

**Date:** 2026-09-12

This ledger supersedes the quantitative-count portions of `META_ANALYSIS_EXTRACTION_STATUS_2026-09-11.md`. The 2026-09-11 file remains a historical extraction checkpoint. The unit of cross-system evidence is now the multilayer cluster defined in `META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-12_MULTILAYER_CLUSTERS.md`.

## Corpus state

- source-verified primary-study seeds: **16**
- candidate systems/programmes: **19**
- priority extraction queue: **9 studies**
- first-pass endpoint extractions materialized before this amendment: **9 studies**
- independent admissible multilayer clusters: **2**
- primary admissible effects inside those clusters: **5** (`PS003`: C/F/G_adult; `PS004`: C/F)
- alternative/sensitivity standardized effect retained outside the primary count: **1** (`PS003` adult `F_IS`)
- separate admissible gradient effects retained as an alternate design stream: **2** (`PS003` C/F Fisher-z effects against `-log(area)`)

No effect row is counted as an independent study merely because it belongs to another biological layer.

## ML001 / PS003 — *Serapias lingua*

The predeclared anthropic populations `C/F/G` and natural populations `A/B/D/E/H/I` define one nine-population cluster. Three primary outcomes use that same contrast and independent-unit frame:

- `C`, pollen immigration: Hedges `g = -10.09901484`, variance `6.16611671`;
- `F`, fruit set: Hedges `g = -4.55409070`, variance `1.65220789`;
- `G_adult`, observed heterozygosity: Hedges `g = -26.07246637`, variance `38.26519459`.

`F_IS` is retained as a sensitivity representation of adult genetics and is not a fourth primary outcome.

The within-cluster covariance block is reconstructed from group-centered paired population outcomes. This is an explicitly labelled sampling-correlation proxy, not a known exact covariance. The 3x3 block is positive definite and is rebuilt in CI from the site table and marginal variances.

## ML002 / PS004 — *Brosimum alicastrum*

The source-defined habitat contrast is the same three continuous versus three fragmented populations. Public Figshare file `Datos-Brosimum.xlsx` (article `22130177`, file id `39338195`, MD5 `049db31f8ebcec42c4c44ebe4a6af70a`) was reanalysed without promoting offspring, maternal trees, individuals or loci to fragmentation replicates.

Two primary layers now satisfy the same six-site effect-unit contract:

- `C`, site-level multilocus correlated paternity `r_p`, oriented as mating/connectivity support: Hedges `g = -2.32153761`, variance `1.11579474`;
- `F`, one-year progeny total dry mass (`TPDW`): Hedges `g = -1.28693964`, variance `0.80468447`.

For `F`, offspring are first averaged within maternal tree and maternal-tree means are then averaged within population. The three populations in each habitat are the independent units.

The paired six-site residual correlation between oriented `C` support and `F` TPDW is `r = 0.67083113`; the resulting 2x2 working covariance block is positive definite and is reconstructed in CI.

Raw adult and progeny microsatellite genotypes were also recovered. Their simple raw `H_O` reconstruction is diagnostic only because it does not yet exactly reproduce the publication-level Table 2 summaries. `G_adult` and `G_offspring` therefore remain `raw_reanalysis_required`; they were not promoted to make the cluster look more complete.

## Standardized-effect variance contract

All admitted binary Hedges-g effects now use one convention: `metafor::escalc(measure="SMD", vtype="LS")`.

`V(g) = 1/n_fragmented + 1/n_reference + g^2 / [2(n_fragmented + n_reference)]`.

The previous mixed use of alternative SMD variance formulas was removed before any cross-system fit. Point estimates were unchanged; only sampling variances and derived covariance blocks were harmonized.

## Gate state

The **comparison gate is open** because two independent clusters now satisfy the multilayer contract:

1. `ML001 Serapias`: `C/F/G_adult`;
2. `ML002 Brosimum`: `C/F`.

This authorizes a covariance-aware cross-system C-F comparison. It does **not** authorize a broad claim that multilayer concordance is general across fragmented plant systems. Additional independent clusters remain required for that claim.

## Cross-system C-F pilot — diagnostic only

The first pilot is calculated at the cluster level, not by treating four C/F effect rows as independent observations. For each cluster:

`delta_F_minus_C = g_F - g_C`

with

`V(delta) = V(F) + V(C) - 2 Cov(F,C)`.

Current cluster contrasts are:

- `ML001 Serapias`: `delta(F-C) = +5.54492414`, variance `4.25650739`, 95% CI `[1.50126267, 9.58858562]`;
- `ML002 Brosimum`: `delta(F-C) = +1.03459796`, variance `0.64917885`, 95% CI `[-0.54457710, 2.61377303]`.

Both independent clusters have `C < 0` and `F < 0`, and in both clusters the connectivity/movement effect is more negative than the reproductive-function effect (`C < F` after common orientation). Thus the current replicated pattern is **directional C-F deterioration with stronger C loss than F loss in 2/2 systems**.

A covariance-aware fixed-effect combination gives diagnostic `delta(F-C) = +1.63145806`, variance `0.56327177`, 95% CI `[0.16047699, 3.10243914]`. Between-cluster dispersion is nontrivial (`Q(df=1)=4.14682905`; descriptive `I2=75.9%`). With only two clusters, these pooled statistics are retained solely as a pipeline/pattern diagnostic; they are not treated as a stable cross-system grand mean or general ecological law.

The main information gained is therefore not a pooled effect size but a sharper next question: whether the apparent ordering `fragmentation -> stronger deterioration in movement/connectivity than realised reproductive function` persists when independent clusters are added, and which biological mechanisms permit F to remain less negative than C.

## Remaining independent-cluster recovery queue

1. `ML003 Spondias`: highest biological layer coverage, but site-level/model-based effect-unit reconstruction is still blocked; lower-level trees/offspring/loci cannot become fragmentation `n`.
2. `ML004 Conospermum 2020`: recover source coefficients/SE or raw population values for a common fragmentation/isolation predictor across `I/F`.
3. `ML005 Conospermum 2026`: recover population-aware `C/G_offspring` under one predeclared landscape predictor; do not concatenate the historical adult cohort.
4. `ML006 Primula`: recover one common landscape exposure before treating published `G/I/F` paths as a fragmentation cluster; current paths use different predictors.

The immediate next recovery target is `ML003 Spondias`, because it can add the broadest independent multilayer test if its site-level/model covariance can be reconstructed without violating the effect-unit firewall. The C-F pilot remains provisional until this independent-cluster set expands.
