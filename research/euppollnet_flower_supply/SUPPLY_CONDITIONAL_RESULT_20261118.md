# Corrected EuPPollNet: bloom-confirmed same-day partition and recorded flower-supply deviations

**Date:** 18 November 2026. **Status:** post-primary exploratory source-exact extension, not an independent experiment, not journal-ready. Empirical `egwee` only; theoretical `egwe` and the frozen fragmentation meta-analysis are not edited.

## Two complementary ecological questions

The pre-outcome PR #72 primary (311 native networks, 39 original programmes) found +0.23232269 nats of wild-bee vs syrphid observed plant-use Jensen–Shannon divergence beyond its same-network finite-count null; see its [primary result](../euppollnet_guild_partition/PRIMARY_RESULT_20261118.md). But the null used **pooled observed visits**, not independent flower availability. The author database also has 199,692 original flower-count records and an exact `Flower_data_merger` field.

The present branch does not rebrand the earlier +0.232 as availability-corrected. It asks two *post-primary*, differently defined source-confirmation questions, with separate frozen design notes and immutable source checks.

### A. Source-locked flower-count coverage: STRICT native record first

The first prospective-for-new-exploratory-work source gate required the same study, network, year, original source `Flower_data_merger` and exact calendar date, homogeneous recorded `Units` within a key, and >=20 guild visits per group plus >=3 source-verified positive flowering plant taxa **per merger key**. Result was **0 qualifying per-merger keys**; do not erase or reinterpret this negative coverage decision.

Source-only database crosswalk established:

- Source interactions **623,476**, original author corrected source SHA256 `6e4e5399338d530462d8683b53a5e564d48e287e423be420c07d8046815ef38a`.
- Original `Flower_counts.csv` **199,692** source records, SHA256 `aaf0474d42ca477e20db75205191f9e64fcd19f78c3e75ae3d66df77a1cefb0a`.
- **196 / 311** original PR #72 eligible network-years share some flower rows before date/merger restrictions.
- **4,365** exact original record-merger+date link keys, originating in **19** original programmes; source `Units` strings include **22** distinct categories overall.
- These links are *individual source co-records*, not 4,365 independent landscape networks or complete multispecies survey units.

[Successful coverage-only CI](https://github.com/zuizui0223/egwee/actions/runs/44234128706).

### B. Assemble the SAME native network and SAME day from exact matched original records

The subsequent scientific unit was explicitly changed in a *new post-coverage note* [DATE_ASSEMBLY_FREEZE_20261118.md](DATE_ASSEMBLY_FREEZE_20261118.md), **before the new daily guild JSD was computed**. The original per-merger result remains zero. Only exact linked merger entries from a common study-network-day are assembled; no broadcasting from nearby days or studies. Restrict to a single nonmissing floral `Units` text, 3 independently counted blooming AND focal visited plant taxa, >=10 guild visits each on counted blooming taxa, and >=70% of all focal visit records for that date included in the matched positive-flower taxon subset.

The source matched **583** original network-days; **213** met all new source-date rules from **18** independent original programmes. Each positive-bloom plant taxon is source-matched using literal accepted names or unambiguous source original→accepted mappings, no fuzzy botanical dictionary repair. Source flower counts are interpreted only as `positive measured bloom` for this question.

| Frozen *post-primary* diagnostic | Result |
|---|---:|
| Qualifying original network×date units | **213** |
| Independent original study programmes | **18** |
| Programmes with positive use divergence | **18/18** |
| Date-equal observed use JSD (descriptive) | **0.28687470 nats** |
| Programme-equal excess JSD after within-date finite-count null | **+0.18872731 nats** |
| Whole original programme bootstrap 95% interval | **[+0.14136375, +0.23686457]** |
| Leave-one-whole-programme mean range | **[+0.17988479, +0.19908368]** |

**Note:** Raw observed JSD is *equal-date*, whereas +0.1887 is *equal-original-programme excess*, and must not be subtracted from the +0.2323 cross-network primary to infer how much supply explained. These analyses have different inclusion frames, time grains and null restrictions. All 199 null shuffles and 2,000 source-programme bootstraps are reproducible from the original source and frozen RNGs.

[Successful bloom-confirmed daily CI](https://github.com/zuizui0223/egwee/actions/runs/44234971138).

### C. Against the actual relative numbers of source-recorded flowers: one signed group contrast

After the positive bloom-confirmed daily result, we prospectively recorded **the distinct, explicitly exploratory** signed flower-count contrast [SUPPLY_RELATIVE_ESTIMAND_FREEZE_20261118.md](SUPPLY_RELATIVE_ESTIMAND_FREEZE_20261118.md) *before calculating these coefficients*. On the **same unchanged 213 dates / 18 programmes** only, a counted positive-flower record contributes to the source-recorded flower count composition; counts are aggregated within source exact matched merger keys, including positive counted taxa with no focal visits.

Per original study-network-date and guild, compare the guild's visit composition to the **within-day distribution of original source-recorded flower units** using Jensen–Shannon divergence; subtract the mean of 199 multinomial draws proportional to the source counted flowers for the guild's finite visit total. Average native dates within original study programme, then average original programmes equally. Both signs of bee-minus-syrphid deviation were equally valid. The main signed group contrast **does not resolve**:

| Flower-supply-relative quantity | Programme-equal value | Source-programme bootstrap 95% interval |
|---|---:|---:|
| Wild bees: excess divergence from recorded flower composition | **+0.12297076 nats** | **[+0.09514819, +0.15799443]** |
| Syrphidae: excess divergence from recorded flower composition | **+0.13085129 nats** | **[+0.10082371, +0.16142019]** |
| **Bees minus Syrphidae** | **−0.00788053 nats** | **[−0.05279001, +0.04092450]** |

- Both guilds have **18/18 positive** programme means of excess departure from this source-recorded flower-count benchmark; this is an exploratory observed-use result, not formal model-based proof of intrinsic preference.
- **8/18** programme-specific signed bee-minus-syrphid contrasts are positive. Whole-original-programme leave-one-out mean contrast: **[−0.02414, +0.000665]**. A possible nonzero difference of either sign remains compatible with uncertainty. **Do not call it equivalence.**
- Median of **9 positively source-counted plant taxa** per eligible native network-date; the count units are not intercalibrated across the 18 original programmes. **10 source rows** with invalid/negative flower counts were excluded by the pre-exposure numeric-validity rule.
- The two guild departures describe *which flowers were used relative to the native source flower-census rows*, not how well pollen was transferred, whether flowers were truly accessible to each guild, or whether seeds survived. Floral count records whose `Flower_data_merger` keys have no corresponding original visitor record can be absent from the reference distribution. Thus the reference is the **exactly source-linked, co-recorded bloom subset**, not an exhaustive independently calibrated whole-flora resource census.

The component bootstrap intervals were added **after the primary signed delta result**, and are therefore secondary post-outcome descriptive precision checks, not a new independent preregistered test. Original author rows, source site names, plant identity/visitation rows and count data remain outside the EGWEE commits.

[Source-hashed recorded-supply result CI](https://github.com/zuizui0223/egwee/actions/runs/44235947704), with derivative-only workflow artifact.

## What is supported, and what is not

**Supported descriptive interpretation:** In numerous independently sourced European networks, wild bees and syrphids visit different proportions of source-matched flowering plant taxa even on coincident study-network dates and after finite-sampling corrections. In the subset with source-recorded floral counts, both guilds exhibit similarly positive observed deviations from a naïve 'visits proportional to recorded flower units' benchmark, while a difference in the *degree* of deviation is unresolved.

**Not established:** Supply-independent biological preference, equal guild selectivity, a competitive coexistence mechanism, exactly concurrent hours/microhabitats, matched accessible nectar/pollen supply, pollen deposition, successful compatible mating, plant fecundity, universal island/fragmentation response, or new validation of the NEE theoretical model. Methodological heterogeneity, spatially uneven bloom sampling, plant-morphology differences in 'flower/inflorescence' units, and source-level selective omission of unvisited taxa are material limitations.

**Prior-art boundary:** Bee/hoverfly plant-use and seasonal guild differences have already been demonstrated (e.g. Lowe et al. 2022, DOI [10.1111/1365-2664.14144](https://doi.org/10.1111/1365-2664.14144); hoverfly-specific resource use and plant trait association in published grassland communities). This analysis contributes an original-programme-weighted, source-corrected, independently co-recorded bloom-date cross-context assessment, **not discovery that bees and hoverflies differ in general**.

**Next meaningful inference gate:** an independent source/region where plant flower supply and observation effort are calibrated to the same area/time and, preferably, plant seed or compatible pollen outcomes are observed on the same source floral unit. The present 213 dates and 18 programmes are source nested within the *same EuPPollNet compilation*, so cannot be counted as external replication of the PR #72 guild result. Do not design additional positive-selection subsets from this result.

## Repository/QA contract

- First-source-only pre-outcome structural coverage: `audit_source_flower_availability.py`, run 44234128706.
- Whole-date amended post-primary bloom-confirmed observational test: `estimate_bloom_confirmed_guild_date.py`, run 44234971138.
- Post-primary source-count relative signed Δ test: `estimate_recorded_supply_deviation.py`, run 44235947704.
- Files are paired with their sequential pre-effect scope/freeze notes and CI.
- Only derivative JSON artifacts are uploaded; source raw flower/visitation records are not committed or redistributed.
- Original PR #72 main result, frozen 5-cluster/17-effect synthesis, PR #63, PoMS, Leavenworthia, theory egwe and submission decisions have not been altered.
