# QPF007 original genetic sire–contact enrichment survives missing partner-row audit

**19 November 2026.** A **post-outcome sensitivity**, following and preserving PR #90's earlier original source-locked co10 result. Source: Barbot et al. (2026), [PLoS Biology 10.1371/journal.pbio.3003579](https://doi.org/10.1371/journal.pbio.3003579); exact original [Zenodo 21628183](https://doi.org/10.5281/zenodo.21628183), original source author R script checked and all original source-file hashes verified. Successful source Actions [run 44545969004](https://github.com/zuizui0223/egwee/actions/runs/44545969004), source-derived artifact 14539937616. This is still **one manipulated original *Brassica rapa* programme, not independent replication**.

## Scientific risk examined

PR #90 observed **688/741** outcross-assigned genetic offspring with **positive** source-inferred `import_nb_visit_co10` contact, 23 source rows with explicit numeric zero, 0 source rows with unknown contact, and **30 genetic offspring whose original mother→father directed pair row was absent entirely**. The registered primary had counted absent rows as **no documented positive evidence**, not as proven zero biological contact, but the null could in principle have many unrecorded pair rows. If a table disproportionately lists genetic successes, a naïve observed-vs-null positive match can be driven by source-row ascertainment.

To test it, an explicitly post-outcome protocol [`QPF007_POSTHOC_ROSTER_ASCERTAINMENT_FREEZE_20261119.md`](QPF007_POSTHOC_ROSTER_ASCERTAINMENT_FREEZE_20261119.md) was committed **before opening three alternative missingness scores**. It retained all original 741 outcross children, 358 source selfed children excluded, 16 original manipulated source sessions (15 swap-exchangeable), precise original direction/father assignment, **10-flower carryover**, and fixed paternal/maternal genotyped-offspring margins. No source cohort, paternity denominator, original co10 metric or outcome was selected after inspecting the alternative signs.

We reran TWO independent source-marginal swaps (RNG 20261125, 20261126, 2,000 draws each, 1,500 burn-in attempts and 100 between recorded null draws per exchangeable source session). Mother and sire genotyped-outcross-offspring counts remain exactly fixed. Every source observation is classified into P = positive source contact, Z = explicitly zero, U = pair row present but source contact unknown, A = entire pair row absent. **Missing A is a documentation gap, not ecological zero**. No original individual IDs, pollen, genotype or visitation row values redistributed.

## Three predeclared challenges, not new independent ecology

| Exact post-outcome source statistic | Observed | Chain 1 expected | Chain 2 expected | Observed−expected |
| --- | ---: | ---: | ---: | ---: |
| **P/N:** documented co10 positive contact | **0.92847503** | 0.80222807 | 0.80254521 | **+0.12625 / +0.12593** |
| **(P+A+U)/N:** all unknown/absent source contacts optimistically treated as positive | **0.96896086** | 0.85046694 | 0.85072807 | **+0.11849 / +0.11823** |
| **(P+Z+U)/N:** merely the presence of an original candidate pair-table row | **0.95951417** | 0.95176113 | 0.95181714 | **+0.00775 / +0.00770** |

Original P/Z/U/A counts are **688 / 23 / 0 / 30**, sum 741; both original and randomized source contact categories were calculated from the **same original source records**. The two chains' null means differ by only **0.00032** for documented positives, **0.00026** for optimistic all-missing contacts and **0.000056** for roster presence, passing the locked 0.01 audit tolerance.

A fourth descriptive ratio conditional on **the changing subset of explicitly measured pair rows** gives **688/711 = 96.765% source-positive**, while the corresponding source-marginal null is **84.289% / 84.317%**, an excess of **+12.48 / +12.45 percentage points**. This conditional-on-row statistic changes its denominator after swaps and **is not** an unbiased independent pollinator-preference estimand. It is a descriptive decomposition of the original source data only.

**The recorded prior source contact enrichment is not dominated by candidate pair-table row presence.** The table-roster-only contrast explains less than one percentage point of excess while the source positivity signal remains larger than 11.8 points even after setting all absent pair rows to positive, under the explicit optimistic imputation on **both** actual and random assignments. The pre-fixed post-outcome condition requiring optimistic excess >0 in both chains and ≥12/16 original session groups supporting it also passed. Decision: **`CONTACT_INFERENCE_SURVIVES_OPTIMISTIC_SOURCE_ROSTER_BOUND`**.

## Claim ceiling and future risks

**Supported within this one experimental source:** inferred pollinator contact between the identified recipient and CERVUS-assigned sire is overrepresented relative to a within-original-session null preserving each individual mother's sampled outcross offspring count and each individual sire's sampled offspring count; this remains positive under the extreme source-missingness assumptions. Thus the association is **not merely an artifact of whether the directed pair appears in the original authors' derived partner table**. This is a valuable sensitivity defense of the narrower PR #90 result.

**Not supported:** that any *absent* partner row was in reality contacted; that positive inferred `import_nb_visit_co10` proves genetic identity of deposited pollen; direct mechanisms of stigma competition, gamete compatibility, seed recruitment, or natural landscape fragmentation; unobserved source observers/effort and CERVUS assignment error fully explained; cross-study or cross-species universal law. `A` and `U` are unresolved observational data, not negative biological contacts. The optimistic imputation is an alternative **explicit assumption**, not an identified interval for the causal contact effect. The 2000-draw conditional Monte Carlo null does not by itself provide cross-study population confidence.

**Important prior-art boundary:** The original Barbot et al. paper already established a pre/postpollination partner mismatch and observational father coverage under long carryover. This is not newly discovered here. The additional EGWEE hypothesis tests whether **pair-specific mating opportunity** carries information over and above the original observed marginal reproductive success totals. Even this robust within-one-programme result requires independent natural or independent experimental studies with same-source plant-pair visits and genetically assigned maternal/sire IDs before any generalization.

PR #90's original analysis [+12.61 pp] and post-hoc [303 unique mother–father genetic pairs +11.70 pp] are not changed. Historical main egwee five-cluster natural fragmentation, other original QPF programmes and separate theoretical `egwe` untouched. The branch is a stacked **draft** PR only, not merged.
