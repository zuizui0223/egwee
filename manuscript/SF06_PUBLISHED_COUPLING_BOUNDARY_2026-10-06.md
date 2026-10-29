# SF06 published coupling boundary — updated after corrected sign parsing (2026-10-07)

## Published aggregate result

Aguilar et al. report, for species with simultaneous land-use effects on pollination and female fitness:

- Pearson r = 0.421;
- P < 0.01;
- n = 82 species.

The simple squared correlation is 0.177. This is a positive average association, not a one-to-one calibration.

## Corrected public-S1 fragmentation result

The accessible public Supplementary Table S1 contains 426 response-labelled physical rows rather than all 500 hierarchical input effects reported in the paper. Within the public-S1 subset, 55 exact habitat-fragmentation pollination–female-fitness pairs are available and 54 have unambiguous constituent-sign consensus after correcting the spaced-minus parser bug.

Their topology is:

| pollination sign | female fitness lower | female fitness nonlower |
|---|---:|---:|
| lower | 35 | 9 |
| nonlower | 7 | 3 |

Thus the best deterministic sign lookup leaves 12/54 mismatches. The result persists under whole-publication and whole-species deletion and in a source-publication-disjoint subset.

## Association versus diagnostic sufficiency

The corrected fragmentation-only Hedges-d model also retains positive continuous coupling:

- beta_pollination = +0.190;
- 95% CI [0.057, 0.324];
- p = 0.0053;
- model R² = 0.069.

Therefore the external evidence now makes the distinction sharper rather than weaker:

- **association:** pollination and female-fitness effects covary positively on average;
- **diagnostic sufficiency:** pollination state does not uniquely identify female-fitness state.

At the binary sign level, knowing pollination sign adds zero classification gain beyond the fragmentation-context baseline in this public subset: always predicting female-fitness decline gives 12/54 errors, the same as the best pollination-sign lookup.

## Compatibility boundary

The preregistered residual compatibility model gives:

- gamma_SC = +0.0639;
- 95% CI [-0.263, +0.390];
- p = 0.701.

The direction is consistent with the original prediction but unresolved. Publication-balanced weighting remains positive but unresolved.

This does not establish self-compatibility as the translation mechanism and does not test effective reproductive assurance directly.

## Claim ceiling

Allowed:

- positive average pollination–female-fitness coupling can coexist with sign-level translation non-identifiability;
- the corrected public-S1 fragmentation subset externally generalizes a many-to-many pollination→female-fitness sign map;
- association and sentinel value are distinct ecological properties;
- nominal compatibility does not resolve the translation in this external test.

Not allowed:

- the 12 sign mismatches are 12 individually significant reversals;
- the public-S1 subset represents all 500 hierarchical inputs used by Aguilar et al.;
- zero incremental binary sign gain implies zero ecological relationship;
- post hoc moderator searching is justified because compatibility is unresolved.
