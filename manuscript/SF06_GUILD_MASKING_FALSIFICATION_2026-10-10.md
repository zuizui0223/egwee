# SF06 pollinator-guild masking hypothesis: exploratory falsification gate (2026-10-10)

## Context and evidential tier

This is a **post hoc diagnostic of the published SF06 public-S1 effects**, not an EGWEE primary meta-analytic result and not evidence of a general guild effect. It adds **zero** quantitative or qualitative programmes to the frozen five-cluster, eight-programme, 16-programme and SF06 denominators. It is part of the empirical **egwee** project, not theoretical egwe.

The ecological candidate is deliberately more specific than “visits do not equal seed set”:

> **Does apparent retention of a vertebrate-mediated pollination signal conceal reproductive decline more often than does the corresponding invertebrate-mediated signal under habitat fragmentation?**

A plausible but *unconfirmed* causal competitor is loss of an effective pollinator, donor-provenance shift, subsequent disperser dependence or resource constraints despite retained upstream counts. The source's pollination-guild label **does not measure any of those mechanisms** and vertebrate pollination must not be equated with vertebrate seed dispersal.

## Deterministic source-level result

We restrict the corrected SF06 public-S1 CSV to habitat-fragmentation publication × species rows with both constituent-consensus **point signs** available (54 pairs, 32 publications). `I nonlower` means the estimated effect was nonnegative, **not** that no biological pollination reduction occurred. A “false-reassurance point sign” is defined as `I nonlower / F lower`. A “false-warning point sign” is `I lower / F nonlower`.

Semicolon-inconsistent metadata are normalized only for the coarse `vertebrate` versus `invertebrate` guild grouping. Categories are source descriptors, not harmonized direct experimental measures of effective service.

| Source frame and guild | Available pairs | I nonlower / F lower | I lower / F nonlower |
|---|---:|---:|---:|
| All: vertebrate | 8 | 3 | 0 |
| All: invertebrate | 46 | 4 | 9 |
| Exclude all source publications overlapping the frozen EGWEE I–F map: vertebrate | 4 | 1 | 0 |
| Exclude overlap: invertebrate | 27 | 3 | 6 |

Within this selected literature corpus only, the observed vertebrate–invertebrate difference in the fraction with apparent false reassurance is **+0.2880** in the full frame (`3/8 - 4/46`) and **+0.1389** in the source-publication-disjoint frame (`1/4 - 3/27`). These are not ecological frequencies or estimated causal risk differences.

## Critical independent-publication deletion

Deleting each entire source publication and recomputing the fraction contrast gives:

- **Full frame:** positive for 32/32 one-publication deletions; the minimum difference is approximately +0.199 after removing Magrach et al. (2013).
- **Source-publication-disjoint frame:** positive for 22/23 deletions, but **negative for 1/23**, specifically removal of **Magrach et al. (2013), _Tristerix corymbosus_**; the comparison then becomes `0/3 - 3/27 = -0.1111`.

Thus the apparent guild difference is **not independently source-robust**, despite the appealing full-corpus contrast. Neither a nominal p value from the 54 nonindependent rows nor a one-sided sign test is an admissible confirmatory finding after exploratory exposure. No discordant SF06 pair has both endpoint signs separately resolved at the 95% level. This analysis cannot identify which biological pathway failed.

For context, the broader 54-pair table has **16 opposite-point-sign rows** (nine `I lower / F nonlower`, seven `I nonlower / F lower`); its previously reported **12** refers to the *minimum deterministic classification mismatches*, **not** the number of opposite-sign pairs.

## Decision

**Hold as a plausible biological moderator to prospectively test; reject it as a present EGWEE headline or a general law.** The current SF06 source composition, stage mismatch and endpoint uncertainty cannot separate guild-specific masking from study/source composition.

The directly falsifiable biological alternatives are:

1. **Guild-linked hidden quality:** for equal observed visitation/pollen quantity and compatible baseline risk, vertebrate-pollinated patches have lower realised outcross/compatible-pollen success or viable offspring. Prediction: calibrated effective-mating measures restore predictive value on fully held-out landscapes.
2. **Guild-independent downstream filter:** masking depends chiefly on microhabitat, seed dispersal, plant condition or postzygotic loss, not pollinator guild. Prediction: conditioning on those measured stage-specific opportunity variables weakens/reverses any guild term.
3. **Literature-composition artifact:** the current difference is a few study-specific signs, not a replicable modifier. Prediction: prospectively sampled and prebalanced independent landscapes do not reproduce the sign/guild interaction.

Study the *same sites, cohorts and season* with visitation/pollen delivery, compatible/outcross mating, viable seed, seed arrival, whole-patch recruitment and detection, and preregister a guild interaction within out-of-landscape validation. Define a biological recruitment target and avoid converting an unmeasured `F nonlower` into true function preservation. Distinguish independent landscape programmes from plants, species, populations, and multiple publications.

## Reproduction and claim boundaries

Run: `python scripts/check_sf06_pollination_guild_mismatch_audit.py`.

The checker reads the corrected frozen `evidence/meta_extraction/sf06_translation_residual_pairs_v1.csv`, shares the existing publication-overlap exclusion, checks source counts and publication deletions, and fails closed on unexpected guild labels. It makes no source download or denominator change.

This is an exploratory **falsification/triage result**. Keep it out of confirmatory abstracts, Figure 5, manuscript headline and effect-family inference unless a future preregistered, independent test earns that promotion.
