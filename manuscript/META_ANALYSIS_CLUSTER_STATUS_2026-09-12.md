# EGWEE multilayer meta-analysis — cluster-first status

**Updated:** 2026-09-15

This ledger is the current cluster-first state. The unit of primary cross-system evidence is the multilayer cluster, not an extracted effect row.

## Corpus state

- source-verified primary-study seeds: **19**
- candidate systems/programmes: **19** plus three post-seed expansions (`PS019 Eucalyptus wandoo`, `PS020 Eucalyptus socialis`, `PS021 Swietenia macrophylla`)
- priority extraction queue: **9 studies**
- independent **primary** admissible multilayer clusters: **4** (`ML001–ML003`, `ML014`)
- primary admissible effects inside those clusters: **11** (`PS003`: C/F/G_adult; `PS004`: C/F; `PS001`: C/G_adult/G_offspring[juvenile]/G_offspring[seed]; `PS020`: G_mating/F)
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

Primary effects:

- `C`, correlated paternity support: `g = -0.25474678`, variance `0.83982293`;
- `G_adult`, adult `H_O`: `g = -0.94088153`, variance `0.92185914`;
- `G_offspring`, juvenile `H_O`: `g = -3.18133069`, variance `1.84541983`;
- `G_offspring`, seed `H_O`: `g = -1.11790599`, variance `0.95830471`.

The defensible result is **representation- and cohort-dependent genetic response**, not a confirmed cohort lag. Juvenile-minus-adult and seed-minus-adult covariance-aware contrasts both cross zero. Four endpoints on five sites give a structurally rank-limited covariance proxy; pairwise components are retained and the full singular matrix is not forced to invert.

## ML014 / PS020 — *Eucalyptus socialis*

ML014 is the fourth primary direct Hedges-g cluster. The recovery contract was committed before public numeric family rows were opened.

Primary source-defined Monarto contrast:

- fragmented = `MONLOW`, isolated-pasture maternal trees/families;
- reference = `MONHIGH`, small-remnant woodland maternal trees/families;
- Yookamurra is source context/sensitivity only and excluded from the primary contrast;
- public complete-case frame = 13 fragmented + 15 reference families.

The source estimates family-level mating parameters and models family-level pollen diversity against family growth. Nearby maternal trees were avoided in source sampling; progeny, loci and repeated growth records remain nested below family. The public family table has 15 rather than the paper's 16 small-remnant mothers; the missing family is not back-filled.

Primary effects:

- `G_mating`, correlated-paternity support (`-r_p`): `g = -1.02391388`, variance `0.16231117`;
- `F`, family mean progeny growth: `g = -0.27180887`, variance `0.14490903`.

Their group-centered paired-family correlation proxy is `rho = +0.32672987`, giving covariance `+0.05010843`; the 2x2 working V is positive definite.

The within-ML014 G_mating-versus-F contrast is `delta=-0.75210501`, SE `0.45497620`, z `-1.65306`, two-sided/cluster `p=0.09831774`. Admission never depended on significance. Biologically this is concordant deterioration with a much stronger mating-support response than progeny-growth response.

The effect-unit audit classifies ML014 as an **individual local-context observational design**, not a replicated landscape experiment. Maternal-family variance does not prove absence of all residual spatial correlation; Yookamurra remains excluded from the primary contrast.

## ML015 / PS019 — *Eucalyptus wandoo* gradient generalisation

ML015 is **not** a primary cluster. It remains in the separate Fisher-z continuous-gradient stream.

Canonical effects:

- `I`, pollen tubes: `z = +0.69029123`;
- `F`, seeds per fruit y2: `z = -0.87593080`;
- `G_adult`, `H_e`: `z = -0.41117288`.

Each marginal variance is `0.125`. The gradient covariance proxy is positive definite. The within-ML015 Bonferroni diagnostic is `p_cluster = 0.00256953`, driven by I-F sign discordance. ML015 contributes zero primary Hedges-g effects and is not combined with the primary Fisher statistic.

## ML016 / PS021 — *Swietenia macrophylla* representation closure

ML016 is a source-verified fifth-cluster candidate but contributes **zero primary effects**.

The source reports strong directional forest-versus-isolated summaries:

- correlated paternity `r_p`: `0.163` forest versus `0.341` isolated;
- five-year common-garden growth: `0.060` forest versus `0.048` isolated.

The source methods state that group mating-system parameter uncertainty was obtained by bootstrapping maternal families. Thus the parenthetical `r_p` uncertainty in Table 1 is not a between-family sample SD that can be combined with `n_family=47/24` in the canonical Hedges-g formula.

Appendix S3 was recovered through the public Europe PMC supplementary package and audited in CI. It contains family-level GLM slope-bootstrap summaries and population-level trend/correlation summaries, not a keyed family table with context, provenance, family `r_p`, and family growth. Therefore neither a valid family-level G_mating Hedges-g representation nor the prespecified paired G_mating/F covariance can be reconstructed from public sources.

Terminal state: `family_level_mating_effect_and_dependence_not_reconstructable`.

This is a **representation boundary, not a biological negative result**. Reopen only with a legitimate source family table containing family id, isolated/forest context, mesic/dry provenance, family `r_p`, and five-year growth. Do not back-solve covariance from regression summaries, digitize Figure 3, set covariance to zero, or treat provenance strata as separate systems.

## Effect-family contract

Primary direct/contrast effects use Hedges g with `metafor::escalc(measure="SMD", vtype="LS")` variance semantics. Continuous gradients use the separate `fisher_z_gradient` stream. Hedges g and Fisher z are never pooled merely to enlarge the primary sample.

## Primary cross-system gates

The primary multilayer denominator remains **4 independent clusters / 11 effects**:

1. `ML001 Serapias`: C/F/G_adult;
2. `ML002 Brosimum`: C/F;
3. `ML003 Spondias`: C/G_adult/G_offspring;
4. `ML014 Eucalyptus socialis`: G_mating/F.

The narrower C-F comparison remains `k=2`; ML014 has G_mating/F rather than C/F. ML015 remains separate gradient generalisation. ML016 is descriptive/source evidence only.

## Formal primary state-separation synthesis

Cluster-level Bonferroni p-values are:

- ML001 Serapias: `0.00354530`;
- ML002 Brosimum: `0.19911670`;
- ML003 Spondias: `0.17406774`;
- ML014 Eucalyptus socialis: `0.09831774`.

Their Fisher combination is `chi-square(8) = 22.6477`, **`p = 0.003847`**, giving `reject_primary_binary_layer_exchangeability`.

Leave-one-primary-cluster-out sensitivity remains important:

- omit ML001: `p = 0.07777` — no rejection;
- omit ML002: `p = 0.00351`;
- omit ML003: `p = 0.00392`;
- omit ML014: `p = 0.00621`.

Thus **ML001 remains influential**. The result is not leave-one-cluster-out robust. ML016 does not change this because it fails the representation/dependence gate before primary admission.

Supported claim:

**Across the four currently admitted direct fragmented-versus-reference systems, the current corpus rejects exchangeability of biological response layers, while the cross-cluster rejection remains dependent on inclusion of ML001 in leave-one-cluster-out sensitivity.**

## Correction provenance

A superseded implementation counted ML015 as a fourth primary cluster and reported p `0.0005347329`; that remains non-canonical. The present fourth primary cluster is ML014, which uses the same direct Hedges-g effect family as ML001–ML003.

## Closed recovery routes and next priority

ML004–ML013 and ML016 are blocked or closed for their recorded source/effect-unit/representation reasons. ML014 is admitted; ML015 is gradient-only. The next empirical upgrade remains an additional independent direct cluster or a genuinely prospective external validation. Do not reclassify gradient, group-bootstrap uncertainty, or nested-unit evidence merely to increase the denominator.
