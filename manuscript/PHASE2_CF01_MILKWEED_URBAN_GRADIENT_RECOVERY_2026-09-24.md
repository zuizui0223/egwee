# Phase-2 CF01 common milkweed urban-gradient recovery — 2026-09-24

## Admission

CFTQ0044 is recovered as one **gradient/generalisation I-F programme**:

- programme: `P2_CF01_MILKWEED_URBAN_2023`;
- peer-reviewed DOI: `10.1007/s11252-022-01278-9`;
- public source repository: `sbreitbart/observ_study_phenotype`;
- pinned source commit: `83e56d790410a134fa099425459aefb6f2d07f12`;
- independent unit: population/patch;
- primary exposure: greater urbanization = negative distance to Toronto urban center;
- primary time frame: 2019.

It contributes **0** to the primary fragmented-versus-reference Hedges-g I-F programme count.

## Primary source-code-faithful frame

The source pollinator analysis constructs abundance from non-zero pollinator observations. Reproducing that behavior and requiring finite 2019 fruit set yields **31 common populations**.

- I, total pollinator abundance per surveyed plant: `r = -0.312450`, Fisher `z = -0.323259`;
- F, mean follicles per inflorescence: `r = 0.104562`, Fisher `z = 0.104946`;
- marginal Fisher-z variance: `0.035714`.

Greater urbanization is associated with lower pollinator abundance but a weakly higher fruit-set endpoint on this common frame.

## I-F response geometry

After residualizing both endpoints on the same urbanization exposure:

- residual I-F correlation: `-0.342785`;
- covariance proxy: `-0.012242`;
- covariance block positive definite: **yes**;
- `I - F = -0.428205`;
- SE `0.309699`;
- z `-1.382649`;
- 95% CI `[-1.035203, 0.178793]`.

The interval crosses zero. This programme therefore suggests opposite-direction I and F gradient responses but does not by itself resolve a statistically precise cross-layer separation.

## Zero-pollinator sensitivity

The source-code construction omits surveyed populations with zero pollinators. A prespecified sensitivity restores the seven valid zero-pollinator common populations:

`MW011, MW028, MW040, MW041, MW042, MW061, MW074`.

This yields **38 common populations**:

- I Fisher z `-0.411279`;
- F Fisher z `0.049724`;
- `I - F = -0.461003`;
- SE `0.263266`;
- 95% CI `[-0.976995, 0.054988]`.

The sensitivity strengthens the negative I-F difference slightly but does not reverse the qualitative response geometry and still crosses zero.

## Phase-2 consequence

Common milkweed becomes the **third** registered gradient/generalisation programme after ML015 Eucalyptus wandoo and P2_CF01_ZURICH_2026.

The primary direct I-F denominator remains **1/5 (ML020 only)**. The four programme families are not pooled: gradient Fisher-z evidence remains a separate secondary/generalisation stream.
