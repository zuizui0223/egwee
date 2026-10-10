# SF06 incremental sentinel-value audit — 2026-10-07

## Status

Post-exposure diagnostic derived from the corrected public-S1 SF06 sign-topology result. This is not a preregistered inferential endpoint and is not a prevalence estimate.

## Question

The corrected external topology establishes that pollination-response sign does not deterministically identify female-fitness sign. A stronger monitoring question is:

**Does knowing pollination-response sign improve binary diagnosis of female-fitness decline beyond the baseline information that the system is fragmented?**

## Full habitat-fragmentation public-S1 subset

The corrected constituent-consensus table for 54 usable paired units is:

| pollination sign | female fitness lower | female fitness nonlower |
|---|---:|---:|
| lower | 35 | 9 |
| nonlower | 7 | 3 |

Thus:

- female fitness is lower in 42/54 = 77.8% of paired units;
- if pollination is lower, female fitness is lower in 35/44 = 79.5%;
- if pollination is nonlower, female fitness is still lower in 7/10 = 70.0%.

The best deterministic lookup from pollination sign to female-fitness sign maps both pollination states to F lower, because F lower is the majority state in both rows.

Therefore:

- baseline rule ignoring pollination (always predict F lower) makes 12/54 errors;
- best pollination-sign lookup also makes 12/54 errors;
- **incremental classification gain from pollination sign = 0 cases**.

The point is not that pollination and fitness are unrelated. The corrected Hedges-d model retains a positive pollination slope (beta=0.1904, 95% CI [0.0565, 0.3243], p=0.00531). Rather, a **positive average amplitude association** does not imply that the upstream sign changes the optimal binary diagnosis of downstream impairment.

## Source-publication-disjoint sensitivity

After deleting every publication that overlaps the frozen EGWEE interaction–function map, the 31-pair consensus table is:

| pollination sign | female fitness lower | female fitness nonlower |
|---|---:|---:|
| lower | 20 | 6 |
| nonlower | 4 | 1 |

Thus:

- baseline always-F-lower errors = 7/31;
- best pollination-sign lookup errors = 7/31;
- incremental classification gain = 0 cases.

This persists in a source-publication-disjoint external subset.

## Ecological interpretation

This separates two properties that are often conflated in ecological monitoring:

1. association — upstream and downstream effects can covary on average;
2. sentinel value — observing the upstream state changes the best diagnosis of downstream impairment.

SF06 supports the first but, at the binary sign level used here, provides no incremental gain for the second.

Combined with the matched-programme EGWEE anchors, the emerging principle is:

> An ecological process can be a valid population-level correlate of function yet add little or no state-diagnostic information about whether function is impaired in a focal fragmented system.

This makes the monitoring question more specific than “is pollination correlated with reproduction?” The relevant question is whether a measured interaction state provides **incremental diagnostic information** beyond fragmentation context and baseline risk.

## Important limits

- The diagnostic table uses point-sign states; only three pairs have both endpoint signs marginally resolved at 95%, and those three are concordant lower/lower.
- The zero-gain result is therefore a structural point-estimate diagnostic, not a clinical-style sensitivity/specificity estimate and not a prevalence estimate.
- Source pairs are literature-derived and can share publications; the source-disjoint sensitivity removes overlap with EGWEE but does not create a random sample of nature.
- This audit does not identify the hidden mechanism. Effective mating, transfer provenance, post-transfer viability and reproductive assurance remain prospective explanatory coordinates.
