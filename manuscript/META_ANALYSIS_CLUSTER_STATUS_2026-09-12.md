# EGWEE multilayer meta-analysis — cluster-first status

**Updated:** 2026-09-13

This ledger is the current cluster-first state. The unit of primary cross-system evidence is the multilayer cluster, not an extracted effect row.

## Corpus state

- source-verified primary-study seeds: **17**
- candidate systems/programmes: **19** plus one post-seed expansion (`PS019 Eucalyptus wandoo`)
- priority extraction queue: **9 studies**
- independent **primary** admissible multilayer clusters: **3** (`ML001–ML003`)
- primary admissible effects inside those clusters: **9** (`PS003`: C/F/G_adult; `PS004`: C/F; `PS001`: C/G_adult/G_offspring[juvenile]/G_offspring[seed])
- standardized sensitivity effects retained outside the primary count: **5** (`PS003` adult `F_IS`; `PS001` adult `Sp` plus adult/juvenile/seed `F_IS`)
- separate admissible Fisher-z gradient effects: **5** (`PS003`: C/F against `-log(area)`; `PS019`: I/F/G_adult against the response-free fragmentation PC)

No endpoint or developmental cohort increases the number of independent systems merely because it is another row. Gradient/generalisation clusters do not increase the primary Hedges-g denominator.

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

The same five sites define the third primary cluster: continuous `Careyes/Chamela` versus fragmented `Mesa/Nacastillo/Ranchitos`.

### Primary effects

- `C`, correlated paternity support: `g = -0.25474678`, variance `0.83982293`;
- `G_adult`, adult `H_O`: `g = -0.94088153`, variance `0.92185914`;
- `G_offspring`, juvenile `H_O`: `g = -3.18133069`, variance `1.84541983`;
- `G_offspring`, seed `H_O`: `g = -1.11790599`, variance `0.95830471`.

`H_O` is primary. Adult `Sp` (`g = +0.50972995`) and adult/juvenile/seed `F_IS` remain alternate genetic sensitivities rather than additional independent G layers.

### Biological boundary

The defensible result is **representation- and cohort-dependent genetic response**, not a confirmed cohort lag.

- juvenile minus adult `H_O`: `delta = -2.24044916`, variance `1.60447392`, 95% CI `[-4.72309301, 0.24219469]`;
- seed minus adult `H_O`: `delta = -0.17702446`, variance `2.44601474`, 95% CI `[-3.24235721, 2.88830829]`.

Neither covariance-aware cohort contrast excludes zero with five sites.

### Dependence

Four co-primary outcomes are retained on five sites. With two habitat groups, the 4x4 empirical covariance proxy is structurally rank-deficient. Pairwise covariance terms are stored; the singular matrix is not forced to invert. Lower-dimensional contrasts use their corresponding components and any future full multivariate fit uses the declared cluster-robust fallback.

Public-source I/F recovery is closed because the supplement does not expose an effect-unit-valid five-site I/F vector or compatible model covariance.

## ML015 / PS019 — *Eucalyptus wandoo* gradient generalisation

ML015 is **not** a fourth primary cluster. The study has no unfragmented/reference group, so the frozen protocol places it in the separate continuous-gradient Fisher-z stream.

Nineteen populations define a response-free fragmentation PC from source descriptors using fixed transforms `-log10(population size)`, `sqrt(isolation)` and `log10(shape)`. The complete common I/F/G frame has 11 populations (`J,K,F,C,E,G,B,I,A,H,D`).

Canonical Fisher-z effects are:

- `I`, pollen tubes: `r = +0.59816906`, `z = +0.69029123`;
- `F`, seeds per fruit y2: `r = -0.70437490`, `z = -0.87593080`;
- `G_adult`, `H_e`: `r = -0.38946811`, `z = -0.41117288`.

Each marginal variance is `1/(11-3)=0.125`. The paired residual-correlation covariance proxy is positive definite with eigenvalues approximately `0.07878`, `0.11796`, `0.17827`.

The state geometry is strongly discordant: pollen quantity rises along the composite fragmentation gradient while realised seed production declines; adult heterozygosity shows a weaker decline. The within-ML015 Bonferroni state-separation diagnostic is `p_cluster = 0.00256953`, driven by the I-F contrast (`z = 3.33386`, two-sided `p = 0.00085651`).

This is generalisation evidence only. It contributes **zero primary Hedges-g effects** and is not combined with the primary cluster Fisher statistic.

## Effect-family contract

Binary/contrast primary effects use Hedges g with `metafor::escalc(measure="SMD", vtype="LS")` variance semantics.

Continuous gradients use the separate `fisher_z_gradient` stream with variance `1/(n-3)` where applicable. Hedges g and Fisher z are never pooled or converted merely to enlarge the primary sample.

## Primary cross-system gates

The primary multilayer denominator is **3 independent clusters / 9 effects**:

1. `ML001 Serapias`: C/F/G_adult;
2. `ML002 Brosimum`: C/F;
3. `ML003 Spondias`: C/G_adult/G_offspring.

The narrower C-F comparison remains `k=2`; the original C-F pooled estimate remains diagnostic rather than a stable grand mean.

ML015 provides a separate natural-system gradient test of I/F/G state separation but does not change the primary denominator.

## Formal primary state-separation synthesis

The corrected formal synthesis tests only ML001–ML003. Within each cluster all admitted endpoint pairs are compared with stored covariance, and the cluster p-value is the Bonferroni-corrected minimum pairwise p-value.

Current cluster p-values are:

- ML001 Serapias: `p_cluster = 0.00354530`;
- ML002 Brosimum: `p_cluster = 0.19911670`;
- ML003 Spondias: `p_cluster = 0.17406774`.

Their Fisher combination is approximately `chi-square(6) = 18.0086`, **`p = 0.00621`**, giving `reject_primary_binary_layer_exchangeability`.

The supported primary claim is therefore:

**across the three currently admitted replicated fragmented-versus-reference systems, biological response layers cannot generally be treated as exchangeable manifestations of one scalar fragmentation response.**

ML015 independently supports the same qualitative state-separation interpretation in the separate gradient tier. Its p-value is not included in the primary Fisher statistic.

## Correction provenance

A superseded implementation counted ML015 as a fourth primary cluster using standardized OLS slopes and reported a four-cluster Fisher p-value of `0.0005347329`. That implementation violates the frozen separation between primary Hedges-g contrasts and continuous Fisher-z gradients and is no longer canonical.

The corrected executable and result are `scripts/synthesize_state_separation.py` and `STATE_SEPARATION_SYNTHESIS_RESULT_2026-09-13.md`.

## Closed recovery routes and next priority

`ML004 Conospermum 2020` is closed as `effect_unit_or_variance_not_reconstructable`; `ML005 Conospermum 2026` is blocked by source access/exposure recovery; `ML006 Primula` lacks a keyed common-population G/I/F table; and ML007–ML013 remain blocked by source access, incompatible estimands, insufficient independent landscape replication, or unreconstructable dependence as recorded in the canonical registry.

The next empirical upgrade is either:

- a genuinely independent **fourth direct fragmented-versus-reference multilayer cluster** admitted under the existing rules; or
- a prospective external validation of the state-separation prediction.

Do not reclassify gradient or nested-unit evidence merely to increase the primary denominator.
