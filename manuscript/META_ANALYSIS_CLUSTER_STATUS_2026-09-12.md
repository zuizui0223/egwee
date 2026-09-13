# EGWEE multilayer meta-analysis — cluster-first status

**Updated:** 2026-09-13

This ledger is the current cluster-first state. The unit of cross-system evidence is the multilayer cluster, not an extracted effect row.

## Corpus state

- source-verified primary-study seeds: **17**
- candidate systems/programmes: **19** plus one admitted post-seed expansion (`PS019 Eucalyptus wandoo`)
- priority extraction queue: **9 studies**
- independent admissible multilayer clusters: **4**
- primary admissible effects inside those clusters: **12** (`PS003`: C/F/G_adult; `PS004`: C/F; `PS001`: C/G_adult/G_offspring[juvenile]/G_offspring[seed]; `PS019`: I/F/G_adult)
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

Spondias supplementary material contains sex ratio (Appendix A) and site-by-cohort genetics (Appendix B), **not site-level visitation or reproductive-function values**. Public-source I/F recovery is closed unless author/raw data provide an effect-unit-valid five-site I/F vector or compatible model covariance.

## ML015 / PS019 — *Eucalyptus wandoo*

This is the fourth independent admissible cluster and the first admitted common-gradient I/F/G_adult system.

Nineteen populations define a response-free fragmentation PC from the three source fragmentation variables. The fixed severity-oriented transforms are `-log10(population size)`, `sqrt(isolation)` and `log10(shape)`. The response-complete common frame contains 11 populations (`J,K,F,C,E,G,B,I,A,H,D`).

Standardized slopes on fragmentation severity are:

- `I`, pollen tubes at the base of the style: `+0.67475197`, bootstrap 95% CI `[+0.20780667, +1.93297843]`;
- `F`, seeds per fruit y2: `-0.79455522`, bootstrap 95% CI `[-1.42507278, -0.22907996]`;
- `G_adult`, unbiased expected heterozygosity `H_e`: `-0.43933127`, bootstrap 95% CI `[-1.59705553, +0.22305372]`.

The paired 10,000-draw population-bootstrap covariance is positive definite; eigenvalues are `0.05688720`, `0.14662690`, `0.30543700`.

This creates a direct natural-system state-separation result: stronger fragmentation is associated with **more pollen tubes but fewer seeds per fruit**, while standing adult genetic diversity has a weaker uncertain decline. Pollination quantity therefore cannot be treated as an interchangeable proxy for reproductive function in this system. The source likewise reports more pollen tubes in smaller populations while seed set increases with population size.

Because aggregate table values were visible during candidate discovery, ML015 is not labelled an outcome-blind preregistration. The exposure reduction itself is response-free and fixed from the three source fragmentation variables, and no endpoint-specific predictor was selected after seeing directions.

## Standardized-effect variance contract

Binary Hedges-g effects use `metafor::escalc(measure="SMD", vtype="LS")`. ML015 is a separately declared standardized-gradient stream with paired population-bootstrap covariance and is not forced into the binary Hedges-g estimator.

## Cross-system gates

The general multilayer comparison denominator is **4 independent clusters**, not 12 effects.

Current primary layer coverage:

1. `ML001 Serapias`: C/F/G_adult;
2. `ML002 Brosimum`: C/F;
3. `ML003 Spondias`: C/G_adult/G_offspring;
4. `ML015 Eucalyptus wandoo`: I/F/G_adult.

The narrower C-F comparison remains `k=2` because neither Spondias nor Eucalyptus wandoo contributes the same C/F estimand. The original C-F pilot remains diagnostic rather than a stable pooled grand mean.

The important new cross-system conclusion is broader: the admitted systems no longer support a single scalar deterioration picture. Serapias and Brosimum show concordant C/F deterioration; Spondias exposes cohort- and representation-dependent genetic response; Eucalyptus wandoo shows direct I-F discordance under one common fragmentation gradient.

## Closed recovery routes

`ML004 Conospermum 2020` is closed as `effect_unit_or_variance_not_reconstructable`; `ML005 Conospermum 2026` is blocked by source access/exposure recovery; `ML006 Primula` lacks a keyed common-population G/I/F table; and ML007–ML013 remain blocked by source access, incompatible estimands, insufficient independent landscape replication, or unreconstructable dependence as recorded in the canonical cluster registry.

The next priority is no longer simply to increase candidate count. It is to test whether the four-cluster geometry supports a defensible cross-layer heterogeneity/state-separation synthesis without pretending that binary Hedges-g and standardized gradient slopes are one interchangeable effect-size family.
