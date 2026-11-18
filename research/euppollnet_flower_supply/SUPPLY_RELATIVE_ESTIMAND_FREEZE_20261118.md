# Recorded-bloom supply-relative bee vs hoverfly use contrast: post-primary estimand freeze

**2026-11-18. Exploratory, NOT independent prospective preregistration.** Written after the positive PR #72 observed-guild JSD and post-primary 213-date/18-programme bloom-confirmed test, **before any source-relative floral-count mismatch coefficient was calculated**. The original native data sources, SHA256 and eligible source group are unchanged. Failure or either effect sign is a valid result.

## Scientific question

In the **same 213 previously selected original network×calendar-date observations**, does source recorded floral-abundance composition differentially explain the plant taxa actually visited by wild bees vs hoverflies? We test **relative use-to-recorded-bloom mismatch**, not flower quality, nectar demand, genuine choice at the same hour, competition or seed set.

Let `q_(t,p)` be the nonnegative original counted flower units for a source-accepted plant taxon p on exact study-network-date t, normalized to sum to one over all mapped, positively recorded flowering taxa, **including unvisited available taxa**. Duplicate original count rows are treated as recorded sampling replicates and summed; no dedup/fuzzy taxonomic repair by outcome inspection. For group g (wild bees or syrphids), `u_(g,t,p)` is the observed interaction count restricted to those positively counted taxa, normalized across the full counted taxon list including zeros.

Define the date-level recorded-supply deviation:

`R_g(t) = JSD(u_g(t), q(t)) − mean_{199 multinomial samples of n_g from q(t)} JSD(simulated_use_g(t), q(t))`

with natural logarithms and `JSD` symmetric. The expected-sampling subtraction corrects the inevitable sample-size divergence when one draws finite visits in proportion to the observed flowers, conditional on q, not on pooled observed visits. A value above zero is excessive observed floral-use deviation relative to a simplistic use-proportional-to-flower-number reference; it is not an effect of selection.

**Sole focal signed contrast:** `Δ_R = R_bee − R_syrphid`. Positive means stronger recorded-supply deviation for bees; negative means stronger deviation for syrphids. Direction **not preselected**. Report R_bee and R_syrphid separately. No use of 0.232/0.189 guild-guild JSD as evidence for a preferred Δ sign. No claim that heterogeneous original flower units are a common global flower-abundance measurement.

## Fixed source/sample/calculation

- Source corrected author `joseblanuza/EuPPollNet@31716d21d5aad8c27c1d91dd0620149ef42e8836`: 623,476 original visits, original 199,692 flower records; exact original-byte SHA256s as in source-coverage contract. Source only, no redistribution.
- Reuse exactly the prior **213** accepted native network×date frames, **18** source programmes, corresponding to the locked 3 positively counted/visited taxa, >=10 focal visits per guild, >=70% exact-merger positive-flower coverage, date and same-Units-label gate. Any drift => stop; no second-source rescue or retroactive gate lowering.
- Date-level source `Flower_count` may have multiple rows per taxon. Sum nonnegative source counts within each strict same-day native network (only original matched merger keys). Never infer abundance from visits. All unique valid source count rows contribute once even if same original taxon repeats. Survey effort/area and whether a unit is a blossom vs inflorescence are unknown in some programmes; record this limitation.
- Use accepted species by exact source accepted name or uniquely observed source original→accepted relation within same network-year; blank/ambiguous/mismatched names excluded. No GBIF synonym guessing.
- Original wild bees by source whitelisted family with `Apis mellifera` excluded, hoverflies source Syrphidae only, and site-year ID 23–25 as one original study programme.
- Exactly **199 independent supply-multinomial draws per guild per accepted date**, default_random seed **20261126**; use zero log zero = 0 and no pseudocounts.
- Average date-level Δ_R equally inside each original programme then average 18 programme means equally, with whole-programme bootstrap **2000** draws, seed **20261127**, 95% percentile range. Report 18 original programme means directional count and LOO range. No sign/prevalence test from the 213 dependent dates.
- As a source-semantic stress test, summarize availability-unit label count and positive supply-taxa count distribution (aggregates only) and total source-matched focal visit coverage. Any critical breach stops rather than replacing the primary with a different measure. Do not adjust/clip implausible flower counts or selectively remove programmes by effect direction.

## Critical interpretation boundaries

This is **one original corrected European network corpus**, not an independent study from PR #72 and not Q→P→F. Recorded flowers per source unit are an imperfect opportunity proxy: surveying individual flowers, inflorescences, plots, floral units and observation hours varies across sources. Therefore **a negative or positive Δ does not establish innate preference, specialized floral morphology, better pollination, compatible pollen or plant reproduction**. It describes a reproducible within-site-date relative discrepancy from a naive supply-proportional visitation model. The source paper already documents source-method heterogeneity; earlier literature already recognizes bee–hoverfly floral-use differences (e.g. Lowe et al. 2022 DOI 10.1111/1365-2664.14144). A new novel biological mechanism would require independent calibrated supply and flower-hour observations plus source-linked pollen and seed-function outcomes.

This test is post-primary exploratory; no submission-ready promotion or change to older PR #72 or the five-cluster synthesis. Store only derivative aggregate result, original source SHA, methodological code and this freeze.
