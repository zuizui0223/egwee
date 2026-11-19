# QPF007 — Source-corrected sire/contact association exceeds a mother–father offspring-marginal null in one experiment

**19 November 2026.** Empirical `egwee`, NOT theoretical `egwe`. Original source: Barbot et al. 2026 *PLoS Biology*, [10.1371/journal.pbio.3003579](https://doi.org/10.1371/journal.pbio.3003579). Original data and code: [Zenodo 10.5281/zenodo.21628183](https://doi.org/10.5281/zenodo.21628183). **Postprimary within-source exploratory quantitative reanalysis; one study / 16 experimental cages/sessions, not 16 independent natural ecological programmes.**

## Original discovery, novel conditional question and outcome freeze

The authors already quantified **observed pollinator contact versus realized genetic mating** and reported that maximal pollen carryover recovered most realized fathers (86.2% of paternal plants under their definition). Pre/postpollination sexual selection and the filtering of high-contact pollen donors are **their discoveries**, not ours. The present, distinct exploratory contrast asks whether father-specific **positive observed/inferred carry-over-10 contact evidence is more common than expected even after conditioning on each original mother and sire's numbers of genotyped outcrossed offspring**. This matters because popular males and well-sampled mothers can generate high apparent contact/paternity agreement without pair-specific ecological information.

Parent PR #89 established source identity: 160 globally unique plant IDs, 16 original sessions, 1,363 directed partner table rows (1,209 exact main-session matched rows; 154 other-session rows excluded), all 1,099 offspring `known_id` and `candidate_id` strings uniquely mapped. The author R script identifies `known_id` as mother for genotype sample counting, `candidate_id` as sire for father reproduction counting, and `session=substr(known_id,1,5)`. The public actual script is `script_ABPOLL_main_analyses.R`; the README uses the singular `script_ABPOLL_main_analysis.R` filename, a documentation discrepancy rather than a missing source. The published CERVUS father assignments use a relaxed **80% confidence** criterion (not certain paternity).

Crucially the **pair table contains potential directed partner records**, not necessarily contacts. For a focal mother receiving pollen from partner/father, we source-authored the exact `(session,ID_full_foc=mother,ID_full_part=father)` pair and `import_nb_visit_co10 > 0` as documented positive contact evidence. A row with explicitly 0 is recorded zero; **a missing pair row is missing source coverage, not proof of no biological contact**. No `seed_couple_on_foc` predictor was used because that response derives from the same paternity assignments and would cause circularity.

Before the first contact values were read on this branch, [`QPF007_CONTACT_NULL_FROZEN_20261119.md`](QPF007_CONTACT_NULL_FROZEN_20261119.md) locked source, biological direction, **10-flower** primary carryover, outcross-only offspring denominator, a within-source-session fixed mother and sire offspring margin randomization, a one-sided conditional Monte Carlo test, session-level bootstrap, minimum number of exchangeable groups, and strict interpretation ceiling. Later sensitivity to carryover and pair-equal weighting was labeled separately rather than used to switch the primary.

## Exact original source data and primary frame

Full source exact published ZIP/Zenodo MD5, source SHA256 for the mother file, directed pair file, parentage file and original R script; source README semantic checksum verified. Original source genotype/plant/offspring rows were never committed.

| Verified original statistic | Source value |
|---|---:|
| Total offspring assigned to an original father | **1,099** |
| Selfed offspring (excluded from visitor-mediated outcross recovery) | **358** |
| Assigned **outcross** offspring included | **741** |
| Original distinct outcross father–mother pairs | **303** |
| Outcross offspring with source-positive carryover-10 contact | **688** |
| Outcross offspring with original pair row explicitly 0 | **23** |
| Outcross offspring lacking original directed pair row | **30** |
| Distinct source experiment sessions | **16**, including **15** exchangeable in the fixed-margin null |
| Outcross source role/session failures | **0** |
| Original direct-pair source in 16 sessions | **1,209** identity-eligible pair rows, not all observed positive |

## Frozen primary: source actual father versus fixed maternal/paternal offspring marginals

The null shuffles original outcrossed offspring's paternal labels **within the same source session**, rejecting a swap whenever it would produce artificial selfing. Therefore every original mother retains the same total number of genotyped outcrossed offspring, every sire retains exactly the same genotyped siring count, and source candidate-pair detection/unknown coverage is left as observed. It does **not** assume every father equally fecund or every mother equally sampled.

Fixed `random.Random(20261119)`, **2,000** complete original-source randomizations, **1,500** warmup and **100** between-draw proposed swaps per exchangeable session. No exchangeable swaps for one original source session, which is held fixed; this is explicitly included in the 16-session descriptive average. Aggregate acceptance **1,434,419/3,022,500 = 47.46%**. Statistical interpretation is conditional on source design, not causal evidence.

| Fixed offspring-weighted primary, carryover 10 flowers | Reproduced |
|---|---:|
| Observed source-positive assigned genetic fathers | **688/741 = 92.8475%** |
| Within-source fixed-marginal null expected fraction | **80.2345%** |
| **Observed minus expected** | **+12.6130 percentage points** |
| Null 2.5–97.5% reference interval (*NOT a confidence interval*) | **78.14%–82.19%** |
| One-sided Monte Carlo p (resolution limit 1/2001) | **0.00049975** |
| Source-session equal mean enrichment | **+13.7199 percentage points** |
| Session-equal 2,000-bootstrap 95% interval, preserving sessions as units | **+7.6487 to +21.4271 percentage points** |
| Sessions with positive difference | **15/16** |
| Pre-fixed bounded *one-source* evidence rule | **PASS** |

**Distinguish estimands:** the original +12.61 pp is **offspring-weighted**. The session-level bootstrap interval applies to the **separate session-equal +13.72 pp estimand**; do NOT present it as the exact confidence interval on the offspring-weighted effect. The null interval is a reference distribution, not the environmental population effect uncertainty.

The CI [run 44475484667](https://github.com/zuizui0223/egwee/actions/runs/44475484667) reproduced the source+frozen primary. It and [rerun 44475834651](https://github.com/zuizui0223/egwee/actions/runs/44475834651) both succeeded without altering the original source eligibility or fixed RNG.

## Fixed, prelisted carry-over sensitivity — primary remains 10

The published original source `import_nb_visit_coXX` records contacts inferred under assumed pollen carry-over lengths, not independently measured donor-specific pollen deposits. The six values below were specified **before opening contact results**. The unselected scenarios do not replace the primary, regardless of their conditional p-values.

| Flower carry-over | Original positive fraction among outcross offspring | Fixed-margin expectation | Excess | Positive source sessions |
|---|---:|---:|---:|---:|
| 1 | 70.58% | 52.68% | **+17.90 pp** | 14/16 |
| 5 | 88.93% | 72.15% | **+16.79 pp** | 15/16 |
| **10 (primary)** | **92.85%** | **80.23%** | **+12.61 pp** | **15/16** |
| 20 | 94.20% | 87.15% | +7.05 pp | 12/16 |
| 50 | 94.74% | 91.86% | +2.87 pp | 8/16 |
| 300 | 95.14% | 93.05% | +2.09 pp | 8/16 |

Each scenario had a one-sided conditional Monte Carlo p at the 2,000-draw resolution floor, but at 50–300 flowers only half the source sessions are above their source-conditioned null means. Saturation of possible contacts under long carry-over greatly reduces the amount of partner discrimination beyond background availability. These are six **highly dependent alternative representations of exactly one original source study**, not independent confirmations of six ecological hypotheses.

## Explicitly retrospective mate-pair weighting and two independent null chains

After the primary, a separate [post-outcome protocol](QPF007_POSTHOC_UNIQUE_PAIR_AND_CHAIN_FREEZE_20261119.md) specified an alternative to counting the same highly fecund genetic pair repeatedly. It deduplicates each mother–father pair *before scoring*, still excluding selfing, and reruns **two independently seeded** exact-marginal swap chains (seeds 20261121 and 20261122, 2,000 draws each) to assess MCMC stability. This is a *post-hoc robustness check*, **not a second preregistered positive result**.

| Genetic-pair-equal postoutcome source statistic | Verified |
|---|---:|
| Distinct assigned outcross mother–father pairs | **303** |
| Positive inferred co10 contact recorded | **270/303 = 89.1089%** |
| Original explicit zero-contact genetic pairs | **14/303** |
| No original candidate pair-table row | **19/303** |
| Chain 20261121 expected fraction | **77.4038%** |
| Chain 20261122 expected fraction | **77.4041%** |
| **Source-pair-equal observed minus expected** | **+11.70 pp** (both chains) |
| Positive original session pair-equal enrichment | **14/16** |
| Pair-equal conditional Monte Carlo p per chain (*exploratory*) | **0.00049975** |
| Difference between independent chain null means | **0.00000226** (pair-equal), **0.00023617** (offspring-weighted) |

The two independent chains agree well within the prewritten 0.01 null-mean audit tolerance. Original source-checksum, original main result and selection decisions are unaffected. [Second independent-chain result, successful CI 44476332447](https://github.com/zuizui0223/egwee/actions/runs/44476332447).

**This matters:** father-specific connection is not an artefact of counting only a few very fecund sire–mother pairs many times. But strong source-dependent pairing does not imply each transferred grain fertilizes equally, nor that the reported father assignments were perfectly accurate or exhaustive.

## Ecological interpretation, prior-art separation and limitations

**Within this experimental source**, flower contact evidence under the original **10-flower pollen carry-over** is associated with actual CERVUS-assigned paternal identity even when the recorded numbers of genotyped offspring per mother and sire are held fixed. The empirical distinction is **who contacted whom**, not simply **who mated most often**. As carryover becomes broader, most genetic father–mother pairs become connected under the assumed visitation history, reducing discriminating information.

**What the original 2026 authors already established:** the existence of an observational versus genetic mating distinction, pollen competition, effects of pollinator density on mating opportunity, and broad apparent recovery of genetic parents from predicted contact; their 86.2% refers to a different carryover/denominator and is **not directly comparable** with the present 92.85% offspring-weighted co10 and 89.11% unique-pair metrics.

**Not identified:** observed individual pollen-grain origin, pollen compatibility, direct genotype-referenced deposition on the sampled stigma, embryo competition, mechanism of filtered genotypes, paternity error, true seedling survival, natural habitat fragmentation, population-level cross-species universal law. Inferred carry-over, experiment-specific source pair roster, genotyping a limited number of seeds per mother, uncertainty in 80% CERVUS father assignments and possible incomplete individual observation may bias the magnitudes. A source row absent from the observed candidate partner table cannot be interpreted as proven absence of flower contact.

The per-offspring permutation p applies to a conditional source-sample null and must **not** be converted into a significance statement from 741 independent ecological populations. There are only **16 manipulated experiment sessions from one study**. The session bootstrap is an internal uncertainty audit, not cross-study meta-analysis.

## Research and repository decision

This result warrants a clearly labeled **one-study conditional-null methodological appendix or source-validated pilot**; it is insufficient for independent macroecological generality. The consequential new cross-study question is whether the degree-preserving contact→assigned-paternity excess recurs in **at least three independent field programmes** after adjusting for source pollinator carryover, completeness of maternal observation, offspring genotyping effort, mating self-compatibility and actual pollen donor availability. Only then can EGWEE test an ecological condition-dependent translation principle rather than a single Brassica author's published mechanism.

All original source files remain at Zenodo. Newly committed work is protocol/source references, source-exact code and workflow, derivative aggregated findings and negative/unstable results. No plant, father, mother, genotype, offspring identities, raw visitation event tables, source numeric rows or individually measured reproductive values are redistributed. Separate QPF007 historical 145-mother confirmatory coverage STOP, PR #88 157-mother genetic mate prediction negative, egwee natural 5-cluster fragmentation synthesis, EuPPollNet, CropPol, other original QPF sources, theory egwe and main remain unchanged.
