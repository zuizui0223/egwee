# EGWEE formal state-separation synthesis — corrected result

**Updated:** 2026-09-15

## Terminal result

`reject_primary_binary_layer_exchangeability_with_influential_ML001_and_separate_gradient_support`

The synthesis preserves the frozen effect-family boundary:

- primary formal inference uses four independently admitted fragmented-versus-reference Hedges-g clusters: ML001, ML002, ML003 and prospectively recovered ML014;
- ML015 *Eucalyptus wandoo* remains a separate Fisher-z gradient generalisation cluster;
- ML015 is not included in the primary Fisher combination.

## Primary cluster-level tests

| cluster | system | admitted primary layers | Bonferroni cluster p | interpretation |
|---|---|---|---:|---|
| ML001 | *Serapias lingua* | C / F / G_adult | 0.00354530 | clear within-system non-exchangeability |
| ML002 | *Brosimum alicastrum* | C / F | 0.19911670 | no individual-cluster rejection |
| ML003 | *Spondias purpurea* | C / G_adult / G_juvenile / G_seed | 0.17406774 | no individual-cluster rejection after six-pair correction |
| ML014 | *Eucalyptus socialis* | G_mating / F | 0.09831774 | concordant deterioration with unequal strength; no individual rejection |

ML014 was recovered under a contract locked before numeric public rows were opened. Its oriented effects are G_mating `g=-1.02391388` and F family growth `g=-0.27180887`; their covariance-aware difference has z=-1.65306 and p=0.09831774.

## Primary cross-cluster synthesis

Fisher combination of the four primary cluster p-values gives:

- Fisher statistic: **22.64771599**
- df: **8**
- combined p: **0.0038472419**

Therefore the current four-primary-cluster corpus rejects the layer-exchangeability null.

## Leave-one-primary-cluster-out sensitivity

The rejection is still **not leave-one-cluster-out robust**:

| omitted cluster | Fisher statistic | df | combined p | reject at 0.05? |
|---|---:|---:|---:|---|
| ML001 Serapias | 11.36345 | 6 | **0.07777** | no |
| ML002 Brosimum | 19.41999 | 6 | **0.00351** | yes |
| ML003 Spondias | 19.15109 | 6 | **0.00392** | yes |
| ML014 Eucalyptus socialis | 18.00861 | 6 | **0.00621** | yes |

ML014 improves the breadth of the primary evidence and shifts the ML001-omission diagnostic from 0.15119 to 0.07777, but ML001 remains influential. The supported claim is therefore the current four-cluster corpus result, not a claim of leave-one-system-out robustness.

## ML014 prospective-recovery boundary

ML014 does not make the whole meta-analysis prospective. The synthesis rule already existed. What was prospective was the recovery of this additional system: before public numeric rows were opened, the contract fixed the Monarto small-remnant versus isolated-pasture contrast, maternal family as the observational unit, family `r_p` as G_mating, family mean growth as F, Hedges-g orientation/variance, and covariance reconstruction. Yookamurra and alternative mating metrics were excluded by that lock.

## Separate ML015 gradient generalisation

ML015 remains on the Fisher-z gradient scale:

- I pollen tubes: `z=+0.69029123`;
- F seeds per fruit y2: `z=-0.87593080`;
- G_adult H_e: `z=-0.41117288`.

Its strongest I-F contrast has z=3.33386, two-sided p=0.00085651; Bonferroni across its three endpoint pairs gives `p_cluster=0.00256953`. This is strong generalisation evidence but is never combined with the primary Hedges-g Fisher statistic.

## What this means

> Across the four currently admitted direct fragmented-versus-reference systems, the corpus-level synthesis rejects exchangeability of biological response layers, but that rejection remains dependent on inclusion of ML001 *Serapias lingua* in leave-one-cluster-out sensitivity.

ML014 adds a distinct geometry: strong deterioration in pollen-donor diversity support with a weaker decline in progeny growth. ML015 separately shows sign-discordant I/F response under a continuous fragmentation gradient.

## What this does not mean

- It does not establish a universal layer ordering.
- It does not imply every cluster individually rejects exchangeability.
- It does not imply leave-one-cluster-out robustness.
- It does not pool Hedges g with Fisher z.
- It does not combine ML015 with the primary Fisher statistic.
- It does not validate a causal operator sequence in nature.
- It is not a prospectively registered meta-analysis.

## Correction provenance

A superseded implementation treated ML015 standardized OLS slopes as a fourth primary cluster and reported p=0.0005347329. That result remains non-canonical. The present four-primary-cluster result arises instead from adding ML014, a direct Hedges-g fragmented-versus-reference system recovered under the existing rules.

Canonical executable: `scripts/synthesize_state_separation.py`.
