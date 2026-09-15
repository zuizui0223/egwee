# EGWEE multilayer meta-analysis — cluster-first status

**Updated:** 2026-09-15

This ledger is the current cluster-first state. The unit of primary cross-system evidence is the multilayer programme/study cluster, not an extracted effect row.

## Corpus state

- source-verified primary-study seeds: **19**
- candidate systems/programmes: **20** plus two post-seed expansions (`PS019 Eucalyptus wandoo`, `PS020 Eucalyptus socialis`)
- priority extraction queue: **9 studies**
- independent **primary** admissible multilayer clusters: **5** (`ML001–ML003`, `ML014`, `ML020`)
- primary admissible marginal effects inside those clusters: **17** (`PS003`: C/F/G_adult; `PS004`: C/F; `PS001`: C/G_adult/G_offspring[juvenile]/G_offspring[seed]; `PS020`: G_mating/F; `PS022`: three dependent species × I/F)
- standardized sensitivity effects retained outside the primary count: **5** (`PS003` adult `F_IS`; `PS001` adult `Sp` plus adult/juvenile/seed `F_IS`)
- separate admissible Fisher-z gradient effects: **5** (`PS003`: C/F against `-log(area)`; `PS019`: I/F/G_adult against the response-free fragmentation PC)

No endpoint, developmental cohort, or species sharing the same programme landscapes increases the number of independent systems merely because it is another row. Gradient/generalisation clusters do not increase the primary Hedges-g denominator.

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

Primary effects:

- `G_mating`, correlated-paternity support (`-r_p`): `g = -1.02391388`, variance `0.16231117`;
- `F`, family mean progeny growth: `g = -0.27180887`, variance `0.14490903`.

Their group-centered paired-family correlation proxy is `rho = +0.32672987`, giving covariance `+0.05010843`; the 2x2 working V is positive definite. The within-ML014 G_mating-versus-F cluster p is `0.09831774`.

## ML020 / PS022 — Aizen–Feinsinger Chaco programme

ML020 is the fifth primary direct Hedges-g programme cluster. It is biologically independent of ML001–ML003/ML014 but was recovered retrospectively: the public Appendix I values were visible during candidate discovery.

The source explicitly replicated three habitat treatments across four Chaco study sites for three species. To avoid selecting a favorable species after seeing results, **all three source-explicit fully replicated species are retained as dependent subsystems inside one programme cluster**:

- *Atamisquea emarginata*;
- *Cercidium australe* (1990 four-site frame);
- *Prosopis nigra* (1990 four-site frame).

Primary contrast and unit:

- fragmented = small forest fragment `<1 ha`;
- reference = continuous forest;
- independent observations for each species/endpoint = four site-specific habitat-unit means per condition;
- plant/flower/fruit counts are nested and are not used as fragmentation replication.

Common endpoints:

- `I`, pollen tubes (`PT`);
- `F`, fruit set (`FS`).

Marginal Hedges-g effects:

- *Atamisquea*: I `g=-0.71203322`; F `g=-1.00369234`; covariance-aware I-F `p=0.79843820`;
- *Cercidium*: I `g=-0.63664333`; F `g=-1.13729930`; I-F `p=0.61865159`;
- *Prosopis*: I `g=-0.48005270`; F `g=-1.13427121`; I-F `p=0.55775444`.

The three species share landscapes and therefore are not three independent Fisher inputs. The frozen programme gate is Bonferroni across the three species-specific I-F tests, giving **`p_ML020=1.0`**. Admission did not depend on significance. Ecologically, ML020 shows fragmentation-associated deterioration in both interaction and reproductive-function layers without detectable separation between their effect magnitudes.

## ML015 / PS019 — *Eucalyptus wandoo* gradient generalisation

ML015 is **not** a primary cluster. It remains in the separate Fisher-z continuous-gradient stream.

Canonical effects:

- `I`, pollen tubes: `z = +0.69029123`;
- `F`, seeds per fruit y2: `z = -0.87593080`;
- `G_adult`, `H_e`: `z = -0.41117288`.

Each marginal variance is `0.125`. The gradient covariance proxy is positive definite. The within-ML015 Bonferroni diagnostic is `p_cluster = 0.00256953`, driven by I-F sign discordance. ML015 contributes zero primary Hedges-g effects and is not combined with the primary Fisher statistic.

## Effect-family contract

Primary direct/contrast effects use Hedges g with `metafor::escalc(measure="SMD", vtype="LS")` variance semantics. Continuous gradients use the separate `fisher_z_gradient` stream. Hedges g and Fisher z are never pooled merely to enlarge the primary sample.

## Primary cross-system gates

The primary multilayer denominator is **5 independent clusters / 17 marginal effects**:

1. `ML001 Serapias`: C/F/G_adult;
2. `ML002 Brosimum`: C/F;
3. `ML003 Spondias`: C/G_adult/G_offspring;
4. `ML014 Eucalyptus socialis`: G_mating/F;
5. `ML020 Aizen–Feinsinger Chaco programme`: three dependent species × I/F, counted once.

ML015 remains separate gradient generalisation.

## Formal primary state-separation synthesis

Cluster-level p-values are:

- ML001 Serapias: `0.00354530`;
- ML002 Brosimum: `0.19911670`;
- ML003 Spondias: `0.17406774`;
- ML014 Eucalyptus socialis: `0.09831774`;
- ML020 Chaco programme: `1.00000000`.

Their Fisher combination is `chi-square(10) = 22.64771647`, **`p = 0.01212432`**, giving `reject_primary_binary_layer_exchangeability` at 0.05.

Leave-one-primary-cluster-out sensitivity is decisive for the claim ceiling:

- omit ML001: `p = 0.18194353` — **no rejection**;
- omit ML002: `p = 0.01276794` — rejection;
- omit ML003: `p = 0.01407214` — rejection;
- omit ML014: `p = 0.02116199` — rejection;
- omit ML020: `p = 0.00384724` — rejection, recovering the prior four-cluster result.

Thus the fifth same-effect-family independent programme answers the targeted robustness question negatively: **the cross-cluster rejection remains materially dependent on inclusion of ML001 Serapias**. ML020 does not reproduce response-layer separation; excluding it because of that result would violate the admission logic.

Supported claim:

**Across five admitted direct fragmentation programme/study clusters, the current corpus rejects exchangeability of biological response layers overall, but that conclusion is not Serapias-independent: omission of ML001 removes the rejection even after admission of a fifth independent same-effect-family programme.**

ML014 remains the prospectively locked recovery; ML020 is a retrospective external recovery retained regardless of its non-significant programme result. ML015 separately supports state separation in the gradient tier.

## Correction provenance and search stop

A superseded implementation counted ML015 as a fourth primary cluster and reported p `0.0005347329`; that remains non-canonical. ML014 is the valid fourth direct Hedges-g cluster. ML020 is the valid fifth direct Hedges-g programme cluster and counts once despite three dependent species subsystems.

The requested fifth-cluster robustness test is now complete. A sixth-cluster search is **not** triggered by the fact that omit-ML001 remains non-significant; any future expansion must be justified by a separately declared coverage goal rather than significance repair.
