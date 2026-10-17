# SF06 sign-margin sensitivity — 2026-10-07

## Status

Post-exposure robustness diagnostic. This was not preregistered and is not used to redefine the primary sign-topology endpoint.

## Question

The primary external topology classifies effects by sign around zero. Some mismatches have small absolute Hedges-d values, so a natural robustness question is whether many-to-many translation disappears after excluding effects close to zero.

We therefore apply a symmetric dead zone to the corrected IVW pair summaries. A pair is retained only when both |d_I| and |d_F| are at least epsilon. The full sweep is reported rather than selecting one favourable threshold.

## Full habitat-fragmentation subset

| epsilon | retained pairs | I−F− | I−F+ | I+F− | I+F+ | minimum mismatches | baseline errors | sign-lookup gain |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 55 | 36 | 9 | 7 | 3 | 12 | 12 | 0 |
| 0.1 | 41 | 30 | 5 | 4 | 2 | 7 | 7 | 0 |
| 0.2 | 31 | 24 | 2 | 3 | 2 | 4 | 4 | 0 |
| 0.3 | 28 | 21 | 2 | 3 | 2 | 4 | 4 | 0 |
| 0.5 | 18 | 13 | 2 | 1 | 2 | 3 | 4 | 1 |

Many-to-many sign translation therefore persists even after requiring both upstream and downstream effects to exceed |d|=0.5.

## Source-publication-disjoint subset

| epsilon | retained pairs | I−F− | I−F+ | I+F− | I+F+ | minimum mismatches | baseline errors | sign-lookup gain |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 32 | 21 | 6 | 4 | 1 | 7 | 7 | 0 |
| 0.1 | 24 | 18 | 3 | 2 | 1 | 4 | 4 | 0 |
| 0.2 | 17 | 13 | 2 | 1 | 1 | 3 | 3 | 0 |
| 0.3 | 14 | 10 | 2 | 1 | 1 | 3 | 3 | 0 |
| 0.5 | 12 | 9 | 2 | 0 | 1 | 2 | 3 | 1 |

Thus the external topology is not generated only by near-zero effects or by publications already used in EGWEE.

## Interpretation

The primary constituent-consensus analysis remains authoritative because it was specified before the corrected result. This margin sweep is a post hoc stress test.

Its useful conclusion is narrower:

> The observed external many-to-many mapping persists across a broad range of zero-exclusion margins, including effect sizes large enough that simple sign jitter around zero is not a sufficient explanation.

At high margins, pollination sign acquires a small amount of incremental binary classification value (one fewer error), but it remains non-identifying.

## Claim ceiling

Allowed:

- external non-identifiability is robust to excluding increasingly large near-zero effect regions;
- mismatch persistence is not solely a zero-threshold artifact.

Not allowed:

- epsilon=0.3 or 0.5 is a biologically validated threshold;
- the threshold sweep is confirmatory;
- error counts estimate population prevalence or operational field error rates.
