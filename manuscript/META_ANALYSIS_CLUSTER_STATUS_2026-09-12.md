# EGWEE multilayer meta-analysis — cluster-first status

**Updated:** 2026-09-13

This ledger is the current cluster-first state. The unit of cross-system evidence is the multilayer cluster, not an extracted effect row.

## Corpus state

- source-verified primary-study seeds: **16**
- candidate systems/programmes: **19**
- priority extraction queue: **9 studies**
- independent admissible multilayer clusters: **3**
- primary admissible effects inside those clusters: **9** (`PS003`: C/F/G_adult; `PS004`: C/F; `PS001`: C/G_adult/G_offspring[juvenile]/G_offspring[seed])
- standardized sensitivity effects retained outside the primary count: **5** (`PS003` adult `F_IS`; `PS001` adult `Sp` plus adult/juvenile/seed `F_IS`)
- separate admissible gradient effects retained as an alternate design stream: **2** (`PS003` C/F Fisher-z effects against `-log(area)`)

No endpoint or developmental cohort increases the number of independent systems merely because it is another row.

## ML001 / PS003 — *Serapias lingua*

One nine-population cluster under the predeclared anthropic (`C/F/G`) versus natural (`A/B/D/E/H/I`) contrast:

- `C`, pollen immigration: `g = -10.09901484`, variance `6.16611671`;
- `F`, fruit set: `g = -4.55409070`, variance `1.65220789`;
- `G_adult`, observed heterozygosity: `g = -26.07246637`, variance `38.26519459`.

`F_IS` remains sensitivity only. The 3x3 paired-population covariance proxy is positive definite and rebuilt in CI.

## ML002 / PS004 — *Brosimum alicastrum*

One six-population cluster under the same three continuous versus three fragmented contrast:

- `C`, site-level multilocus correlated paternity `r_p`, oriented as support: `g = -2.32153761`, variance `1.11579474`;
- `F`, one-year progeny total dry mass (`TPDW`): `g = -1.28693964`, variance `0.80468447`.

The paired C-F residual correlation is `r = 0.67083113`. Raw genotype reconstruction remains QA-pending and is not promoted merely to add genetic layers.

## ML003 / PS001 — *Spondias purpurea*

The same five sites define the third cluster: continuous `Careyes/Chamela` versus fragmented `Mesa/Nacastillo/Ranchitos`.

### Primary effects

Appendix B resolves site-specific genetic values by developmental stage, so the earlier habitat-summary effect-unit block is removed without using individual counts or locus SD as replication.

- `C`, correlated paternity support: `g = -0.25474678`, variance `0.83982293`;
- `G_adult`, adult `H_O`: `g = -0.94088153`, variance `0.92185914`;
- `G_offspring`, juvenile `H_O`: `g = -3.18133069`, variance `1.84541983`;
- `G_offspring`, seed `H_O`: `g = -1.11790599`, variance `0.95830471`.

`H_O` is primary because the same rule was already used for Serapias. Adult `Sp` (`g = +0.50972995`) is retained as structural sensitivity, and adult/juvenile/seed `F_IS` are retained as alternate genetic sensitivities rather than additional independent G layers.

### What changed biologically

The previous provisional interpretation based on adult `Sp` alone — contemporary C deteriorates while adult G does not — is too strong. Canonical adult `H_O` also declines under fragmentation. The defensible result is instead **representation- and cohort-dependent genetic response**.

The point estimates suggest stronger juvenile than adult heterozygosity deterioration:

- juvenile minus adult `H_O`: `delta = -2.24044916`, variance `1.60447392`, 95% CI `[-4.72309301, 0.24219469]`;
- seed minus adult `H_O`: `delta = -0.17702446`, variance `2.44601474`, 95% CI `[-3.24235721, 2.88830829]`.

Neither covariance-aware cohort contrast excludes zero with only five sites. Therefore Spondias is a **cohort-lag candidate**, not a confirmed cohort-lag result.

### Dependence

Four co-primary outcomes are retained on five sites: C, adult H_O, juvenile H_O and seed H_O. With two habitat groups, within-habitat residual dimension is only `5-2=3`, so the empirical 4x4 covariance proxy is structurally rank-deficient. Pairwise covariance terms are stored and audited; the singular 4x4 proxy is not forced to invert. Lower-dimensional cohort contrasts use their corresponding 2x2 covariance components, while any future full multivariate fit uses the declared cluster-robust fallback.

## Standardized-effect variance contract

All admitted binary Hedges-g effects use `metafor::escalc(measure="SMD", vtype="LS")`:

`V(g) = 1/n_fragmented + 1/n_reference + g^2 / [2(n_fragmented + n_reference)]`.

## Cross-system gates

The general multilayer comparison denominator is **3 independent clusters**, not 9 effects.

Current layer overlap is uneven:

1. `ML001 Serapias`: C/F/G_adult;
2. `ML002 Brosimum`: C/F;
3. `ML003 Spondias`: C/G_adult/G_offspring.

The narrower C-F comparison remains `k=2` because Spondias still lacks effect-unit-valid site-level F. The C-F pilot is unchanged: both Serapias and Brosimum have C<0 and F<0, with C more negative than F; pooled numbers remain diagnostic at k=2.

The C-G_adult overlap is now also `k=2` (Serapias and Spondias) on the same canonical `H_O` representation. Given extreme between-system magnitude differences and small cluster count, it is suitable for diagnostic geometry, not a stable pooled grand mean.

## Closed recovery routes and next queue

Spondias supplementary material contains sex ratio (Appendix A) and site-by-cohort genetics (Appendix B), **not site-level visitation or reproductive-function values**. Public-source I/F recovery is therefore closed at the current representation boundary; reopen only if author/raw data provide an effect-unit-valid five-site I/F vector or compatible model covariance. Missing I/F are not inferred from significance statistics.

`ML004 Conospermum 2020` is also closed as `effect_unit_or_variance_not_reconstructable` after the Elsevier supplement and thesis/repository audit. Its biological directions remain source-supported, but no same-exposure population/model effect pair with compatible uncertainty/covariance is publicly recoverable; the 2019 reproductive dataset is not imported as a synchronized rescue.

The next independent-cluster priority is now:

1. `ML005 Conospermum 2026`: use public Dryad adult/seedling microsatellite data plus the source-defined landscape/matrix context to attempt a population-aware `C/G_offspring` cluster without duplicating the historical adult cohort;
2. `ML006 Primula`: recover one common landscape exposure before G/I/F can become one fragmentation cluster.

The main cross-system question is now sharper: **which biological layers deteriorate synchronously, which decouple, and when do apparent lags depend on genetic metric or developmental cohort?**
