# SF06 reproductive-severity diagnostic threshold sweep — 2026-10-07

## Status

Post-exposure stress test of the manuscript title and sentinel interpretation. The thresholds were examined together and are not promoted as biologically validated cut points.

## Question

The primary sign diagnostic defines reproductive decline as d_F < 0. A stronger challenge is whether pollination becomes a useful stand-alone diagnostic if the target is restricted to **larger** female-fitness declines.

For each threshold T in {0, -0.2, -0.5, -0.8, -1.0}:

- target state = d_F < T;
- continuous pollination score = -d_I, so larger values indicate stronger pollination decline;
- report empirical AUC;
- separately compare the best binary lookup from pollination sign with the majority-state baseline.

## Full habitat-fragmentation public-S1 subset

| female-fitness threshold | target cases / 55 | pollination AUC | baseline errors | pollination-sign lookup errors | sign gain |
|---:|---:|---:|---:|---:|---:|
| 0.0 | 43 | 0.587 | 12 | 12 | 0 |
| -0.2 | 36 | 0.604 | 19 | 17 | 2 |
| -0.5 | 24 | 0.641 | 24 | 24 | 0 |
| -0.8 | 13 | 0.612 | 13 | 13 | 0 |
| -1.0 | 12 | 0.607 | 12 | 12 | 0 |

Across this full threshold sweep, continuous pollination effects show only weak-to-moderate discrimination and pollination sign rarely improves the majority-state classification rule.

## Source-publication-disjoint subset

| female-fitness threshold | target cases / 32 | pollination AUC | baseline errors | pollination-sign lookup errors | sign gain |
|---:|---:|---:|---:|---:|---:|
| 0.0 | 25 | 0.571 | 7 | 7 | 0 |
| -0.2 | 20 | 0.613 | 12 | 11 | 1 |
| -0.5 | 17 | 0.706 | 15 | 12 | 3 |
| -0.8 | 10 | 0.605 | 10 | 10 | 0 |
| -1.0 | 9 | 0.585 | 9 | 9 | 0 |

The moderate AUC at d_F < -0.5 is an important boundary: pollination is not information-free. For one post hoc severity threshold it has appreciable ranking value in the source-disjoint subset.

But this does not restore stand-alone diagnostic sufficiency:

- the relationship is threshold-dependent rather than stable;
- sign-based decisions remain non-identifying;
- publication-LOO severity prediction gains are only a few percent;
- the threshold was not biologically predeclared.

## Implication for wording

The evidence supports:

> **pollination tracks reproductive decline but is an insufficient stand-alone diagnostic/sentinel of reproductive state.**

It does **not** support the stronger claim that pollination contains zero diagnostic information.

The current short title phrase “tracks but does not diagnose” should therefore be read as a sufficiency statement: pollination alone does not determine or reliably transfer-diagnose reproductive state across systems.

## Claim ceiling

Allowed:

- diagnostic value is weak and threshold-dependent rather than absent;
- pollination is insufficient as a stand-alone sentinel;
- the result persists across several definitions of reproductive decline.

Not allowed:

- AUC is universally near 0.5;
- pollination has no useful information at any severity threshold;
- d_F=-0.5 is an ecologically validated threshold;
- this post hoc sweep is confirmatory.
