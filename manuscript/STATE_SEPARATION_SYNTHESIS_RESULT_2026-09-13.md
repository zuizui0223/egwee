# EGWEE formal state-separation synthesis — corrected result

**Updated:** 2026-09-15

## Terminal result

`reject_primary_binary_layer_exchangeability_with_influential_ML001_after_fifth_cluster_and_separate_gradient_support`

The synthesis preserves the frozen effect-family boundary:

- primary formal inference uses five independently admitted direct fragmented-versus-reference Hedges-g programme/study clusters: ML001, ML002, ML003, prospectively recovered ML014, and retrospectively recovered ML020;
- ML020 contains three species sharing the same four Chaco landscapes and therefore counts as **one** independent programme cluster, not three systems;
- ML015 *Eucalyptus wandoo* remains a separate Fisher-z gradient generalisation cluster and is not included in the primary Fisher combination.

## Primary cluster-level tests

| cluster | system | admitted primary layers | Bonferroni cluster p | interpretation |
|---|---|---|---:|---|
| ML001 | *Serapias lingua* | C / F / G_adult | 0.00354530 | clear within-system non-exchangeability |
| ML002 | *Brosimum alicastrum* | C / F | 0.19911670 | no individual-cluster rejection |
| ML003 | *Spondias purpurea* | C / G_adult / G_juvenile / G_seed | 0.17406774 | no individual-cluster rejection after six-pair correction |
| ML014 | *Eucalyptus socialis* | G_mating / F | 0.09831774 | concordant deterioration with unequal strength; no individual rejection |
| ML020 | Aizen–Feinsinger Chaco programme | I / F | 1.00000000 | pollination and fruit-set deterioration are not detectably separated under the frozen programme gate |

ML014 was recovered under a contract locked before numeric public rows were opened. Its oriented effects are G_mating `g=-1.02391388` and F family growth `g=-0.27180887`; their covariance-aware difference has z=-1.65306 and p=0.09831774.

ML020 is a retrospective external recovery. The source Appendix I was visible during candidate discovery, so outcome-blind discovery is not claimed. To prevent within-paper selection, all three species explicitly identified by the source as having the three habitat treatments replicated across four sites were retained: *Atamisquea emarginata*, *Cercidium australe*, and *Prosopis nigra*. For each, the primary contrast is small fragment versus continuous forest, using one site-specific habitat-unit mean per site, PT as I and fruit set as F. The three species-specific covariance-aware I-F p-values are 0.79843820, 0.61865159 and 0.55775444; the predeclared within-programme Bonferroni gate is therefore `p_ML020=1.0`.

## Primary cross-cluster synthesis

Fisher combination of the five primary cluster p-values gives:

- Fisher statistic: **22.6477164713**
- df: **10**
- combined p: **0.0121243241**

Therefore the current five-primary-cluster corpus rejects the layer-exchangeability null at 0.05. The Fisher statistic is unchanged from the four-cluster result because ML020 contributes `-2 log(1)=0`; the additional degrees of freedom make the combined p-value less extreme.

## Leave-one-primary-cluster-out sensitivity

The rejection remains **not leave-one-cluster-out robust**:

| omitted cluster | Fisher statistic | df | combined p | reject at 0.05? |
|---|---:|---:|---:|---|
| ML001 Serapias | 11.36345148 | 8 | **0.18194353** | no |
| ML002 Brosimum | — | 8 | **0.01276794** | yes |
| ML003 Spondias | — | 8 | **0.01407214** | yes |
| ML014 Eucalyptus socialis | — | 8 | **0.02116199** | yes |
| ML020 Chaco programme | 22.64771647 | 8 | **0.00384724** | yes |

The fifth same-effect-family cluster therefore answers the targeted robustness question negatively: **the primary cross-system rejection does not survive removal of ML001 Serapias**. The omit-ML001 p-value moves from 0.07777 in the four-cluster corpus to 0.18194 after admitting ML020 because the independent Chaco programme shows concordant rather than separated I/F responses.

This is the desired independent-system test, not a reason to discard ML020 or search for a replacement system based on significance.

## Recovery-boundary provenance

### ML014

ML014 does not make the whole meta-analysis prospective. What was prospective was the recovery of this additional system: before public numeric rows were opened, the contract fixed the Monarto small-remnant versus isolated-pasture contrast, maternal family as the observational unit, family `r_p` as G_mating, family mean growth as F, Hedges-g orientation/variance, and covariance reconstruction. Yookamurra and alternative mating metrics were excluded by that lock.

### ML020

ML020 is independent in biological system and landscape programme, but retrospective at discovery. Its role is especially informative because admission was based on effect-unit validity, common effect-family membership, and reconstructed dependence—not on producing a small p-value. The source-explicit multi-species replication was retained as one programme cluster and its non-separating result was carried into the synthesis unchanged.

## Separate ML015 gradient generalisation

ML015 remains on the Fisher-z gradient scale:

- I pollen tubes: `z=+0.69029123`;
- F seeds per fruit y2: `z=-0.87593080`;
- G_adult H_e: `z=-0.41117288`.

Its strongest I-F contrast has z=3.33386, two-sided p=0.00085651; Bonferroni across its three endpoint pairs gives `p_cluster=0.00256953`. This is strong generalisation evidence but is never combined with the primary Hedges-g Fisher statistic.

## What this means

> Across five currently admitted direct fragmentation programme/study clusters, the corpus-level synthesis rejects exchangeability of biological response layers overall, but that rejection remains materially dependent on inclusion of ML001 *Serapias lingua*. A fifth independent same-effect-family programme did not reproduce response-layer separation and strengthened the evidence that the present general claim must remain conditional.

ML020 also clarifies an ecological distinction: fragmentation can depress interaction and reproductive-function layers together without requiring those layers to differ in effect magnitude. Thus “fragmentation affects multiple states” is broader than “fragmentation separates state responses.”

## What this does not mean

- It does not establish a universal layer ordering.
- It does not imply every cluster individually rejects exchangeability.
- It does not imply leave-one-cluster-out robustness.
- It does not pool Hedges g with Fisher z.
- It does not combine ML015 with the primary Fisher statistic.
- It does not validate a causal operator sequence in nature.
- It is not a prospectively registered meta-analysis.
- It does not justify searching for a sixth cluster merely to restore Serapias-independent significance.

## Correction provenance

A superseded implementation treated ML015 standardized OLS slopes as a fourth primary cluster and reported p=0.0005347329; that result remains non-canonical. ML014 is the valid fourth direct Hedges-g cluster. ML020 is the valid fifth direct Hedges-g programme cluster and counts once despite containing three dependent species subsystems.

Canonical executable: `scripts/synthesize_state_separation.py`.
