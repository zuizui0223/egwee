# EGWEE multilayer meta-analysis — cluster-first status

**Date:** 2026-09-12

This ledger supersedes the quantitative-count portions of `META_ANALYSIS_EXTRACTION_STATUS_2026-09-11.md`. The 2026-09-11 file remains a historical extraction checkpoint. The unit of cross-system evidence is now the multilayer cluster defined in `META_ANALYSIS_PROTOCOL_AMENDMENT_2026-09-12_MULTILAYER_CLUSTERS.md`.

## Corpus state

- source-verified primary-study seeds: **16**
- candidate systems/programmes: **19**
- priority extraction queue: **9 studies**
- first-pass endpoint extractions materialized before this amendment: **9 studies**
- independent admissible multilayer clusters: **3**
- primary admissible effects inside those clusters: **7** (`PS003`: C/F/G_adult; `PS004`: C/F; `PS001`: C/G_adult)
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

## ML003 / PS001 — *Spondias purpurea*

The same five study sites define the third independent multilayer cluster: continuous `Careyes/Chamela` versus fragmented `Mesa/Nacastillo/Ranchitos`.

Two source tables provide one site-level estimate per independent site:

- `C`, multilocus correlated paternity `r_p` from Table 3, oriented as mating/connectivity support: Hedges `g = -0.25474678`, variance `0.83982293`;
- `G_adult`, spatial genetic structure strength `Sp` from Table 2, oriented so stronger fragmentation-induced SGS is deterioration: Hedges `g = +0.50972995`, variance `0.85931580`.

The C and adult-G effects therefore do **not** form a simple concordant deterioration pattern. Contemporary sire-pool support is lower under fragmentation while standing adult spatial genetic structure does not shift in the same deterioration direction. This is retained as a cross-layer state-separation result, not reinterpreted as an absence of fragmentation effects.

Using the five paired sites, the group-centered oriented C-G correlation proxy is `r = -0.44037050`, giving covariance `-0.37410066`. The 2x2 working covariance block is positive definite and is rebuilt in CI. The diagnostic paired contrast `G_adult - C = +0.76447673` has variance `2.44734005` and a broad 95% CI `[-2.30174269, 3.83069615]`; with five sites this contrast is descriptive rather than a standalone inferential claim.

Importantly, no lower-level observation was promoted to make ML003 qualify. Pollinator visitation and fruit-set remain source-model/site-reconstruction targets; pollen-distance offspring events remain nested; `H_O/F` cohort summaries remain blocked where individual counts and locus-level dispersion are incompatible.

## Standardized-effect variance contract

All admitted binary Hedges-g effects use one convention: `metafor::escalc(measure="SMD", vtype="LS")`.

`V(g) = 1/n_fragmented + 1/n_reference + g^2 / [2(n_fragmented + n_reference)]`.

The previous mixed use of alternative SMD variance formulas was removed before any cross-system fit. Point estimates were unchanged; only sampling variances and derived covariance blocks were harmonized.

## Gate state

The **general multilayer comparison gate is open at three independent clusters**:

1. `ML001 Serapias`: `C/F/G_adult`;
2. `ML002 Brosimum`: `C/F`;
3. `ML003 Spondias`: `C/G_adult`.

This is the first state in which the evidence is no longer one-system or two-system only. It still does **not** authorize a broad pooled grand mean across all layers: the three clusters have different overlapping layer sets, small independent-unit counts and visibly different cross-layer geometry.

The narrower **C-F comparison remains a two-cluster analysis**, because Spondias does not yet have an effect-unit-valid F estimate on the same five-site scale.

## Cross-system C-F pilot — diagnostic only

The C-F pilot is calculated at the cluster level, not by treating four C/F effect rows as independent observations. For each qualifying cluster:

`delta_F_minus_C = g_F - g_C`

with

`V(delta) = V(F) + V(C) - 2 Cov(F,C)`.

Current cluster contrasts are:

- `ML001 Serapias`: `delta(F-C) = +5.54492414`, variance `4.25650739`, 95% CI `[1.50126267, 9.58858562]`;
- `ML002 Brosimum`: `delta(F-C) = +1.03459796`, variance `0.64917885`, 95% CI `[-0.54457710, 2.61377303]`.

Both C-F clusters have `C < 0` and `F < 0`, and in both the connectivity/movement effect is more negative than the reproductive-function effect. A covariance-aware fixed-effect diagnostic gives `delta(F-C) = +1.63145806`, variance `0.56327177`, 95% CI `[0.16047699, 3.10243914]`, with `Q(df=1)=4.14682905` and descriptive `I2=75.9%`.

With only two C-F clusters, these pooled statistics remain pipeline/pattern diagnostics rather than a stable cross-system grand mean. ML003 strengthens the broader state-separation claim but does not increase the C-F denominator.

## Remaining independent-cluster / layer recovery queue

1. `ML003 Spondias`: now admitted as `C/G_adult`; next recover I or F on the same five-site scale to connect the state-separation result to realised interaction/function.
2. `ML004 Conospermum 2020`: recover source coefficients/SE or raw population values for a common fragmentation/isolation predictor across `I/F`.
3. `ML005 Conospermum 2026`: recover population-aware `C/G_offspring` under one predeclared landscape predictor; do not concatenate the historical adult cohort.
4. `ML006 Primula`: recover one common landscape exposure before treating published `G/I/F` paths as a fragmentation cluster; current paths use different predictors.

The next high-value question is no longer merely whether another cluster exists. It is whether additional systems reproduce one of the now-observed cross-layer geometries: concordant deterioration (`Serapias`), stronger process than function loss (`Brosimum`), or contemporary-process/adult-genetic separation (`Spondias`).
