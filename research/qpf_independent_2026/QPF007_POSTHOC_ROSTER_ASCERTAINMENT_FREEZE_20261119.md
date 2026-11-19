# QPF007: whether the fixed-parent-margins contact enrichment is actually pair-ROSTER ascertainment

**2026-11-19. Explicitly post-outcome, challenge analysis.** Original PR #90 co10 source result was already seen: **688/741** outcrossed assigned offspring had documented positive inferred co10 contact, **23/741** had an explicit source zero, **30/741** lacked a directed mother→father pair row. A 2,000-draw within-session parent-offspring-marginal null gave **80.2345%** documented positives, excess **+12.613 percentage points**. The source original biological effect, code, protocol and resulting positive decision are historically immutable. Here we deliberately test **how much of that enrichment comes from missing directed pair rows**, rather than asserting that an absent partner row means zero actual contact.

## Hypothesis, predeclared before running new alternative-imputation scores

If a candidate directed pair table contains rows disproportionately selected from actual mating pairs, an apparently positive co10 contact indicator may be dominated by **whether a row exists in that derived table**. The old statistic is a valid *documented-positive joint event* but not a clean ecological contact probability if source row ascertainment depends on genotyped paternal identity. A study may overstate identification if it combines the nonrandom roster with inferred contacts.

Source stays Barbot et al. 2026, PLoS Biology [10.1371/journal.pbio.3003579](https://doi.org/10.1371/journal.pbio.3003579), exact original source at [Zenodo 21628183](https://doi.org/10.5281/zenodo.21628183), fixed SHA256 checks in parent source parser. One original experiment, 16 manipulated experimental sessions, **741** assigned outcrossed offspring; source paternal assignment at 80% CERVUS threshold, non-observed directed pairs not known biological zeros. No new independent study.

### Frozen retrospective source-accounting checks

Do **not** change co10, source eligibility, excluded self offspring, original pair direction, 1,209 original pair roster, or fixed mother and father offspring margins. Define, for each outcross offspring in every null draw, mutually exclusive categories:
- `P`: directed pair row exists and co10 source numeric is strictly positive
- `Z`: directed pair row exists and co10 source numeric explicitly equals zero
- `U`: directed pair row exists but co10 source numeric is missing / NA
- `A`: no directed pair row exists for the original mother→father genotype pair.

For actual and randomized mother–father assignments, output exact counts of P/Z/U/A, and grouped proportions. The original registered statistic is `P/N`, which treats U/A as *no documented positive evidence*, NOT as proven zero ecological contact.

Compare three **prelisted and jointly reported** contrasting estimands for the same source offspring:
1. **Documented positive** = P/N. This must exactly reproduce **688/741** for observed original data and the previous +12.61 pp primary expectation within Monte Carlo error; not a replacement for it.
2. **Optimistic absent-row bound** = (P+A+U)/N, treating **ALL** missing source rows and missing contact values as possible positive contacts, for both observed and null label permutations. For a given fixed dataset this provides a bound on the source-positive proportion, but *not* a sharp causal bound on the difference (which depends on missingness allocation and the null). The null expectation under this explicit imputation is informative; if the sign reverses, the original excess depends on the source roster.
3. **Roster presence** = (P+Z+U)/N, irrespective of contact value. If the original observed-vs-null excess mainly comes from disproportionate row presence, describe that as **data-availability/pair-selection information**, not observed bumblebee transfer.
4. **Positive among source-measured rows** = P/(P+Z) if denominator nonzero; compare actual ratio with null draws' ratios *descriptively only*. This **conditions on a postulated subset that changes under permutation** and must not be interpreted as unbiased pollinator choice or as an independent significance test. Provide the null ratio and observed/expected support counts. The original source exclusion/coding cannot be amended after seeing this outcome.

### Null and auditing

Two **independent** fixed mother/father offspring-marginal swap chains, RNG seeds **20261125** and **20261126**, **2,000** complete randomized replicates each, **1,500** attempted warm-up swaps and **100** attempted between-draw swaps per exchangeable original session, 15 session groups exchangeable; reject swaps that would create selfing. Check the 741 outcross offspring total, original parent-role/session mapping, known source positive/zero/absent category counts, and every mother's and sire's original genetic offspring degree after permutation. Each chain computes original and all four alternative means, empirical 95% permutation quantiles and observed-minus-null excess; display source-roster/optimistic results for both chains without selection. The reproducibility threshold is **max |two chain expected fraction differences| <=0.01** for all three unconditional fractions; violation is an MC mixing warning, not a reason to change primary direction.

**Critical interpretation gate:** call the PR #90 original finding **contact-robust to unknown pair roster** only if the documented-positive excess stays positive **AND** the optimistic missing-as-positive excess stays positive in **both chains** AND at least 12/16 original sessions support the optimistic excess when compared to their within-session null expected value. Otherwise label **`CONTACT_ASSOCIATION_DEPENDS_ON_ROSTER_ASCERTAINMENT`**, preserving the original PR #90 primary statistical value but lowering the ecological claim to source-documented positive evidence. This gate is retrospective and must not be called a preregistered new positive result.

### No scientific leakage

No original genotype/mother/offspring IDs or observation rows distributed, no editor or PR changes to original registered co10 or historical 303 pair-equal result. Do not infer a new mechanism/competing pollen quality if signs differ. A reversal would be informative because it shows that the apparent additional identity information may reflect how the original source authors compiled the directed pair-table rows.

Source code and results are *postprimary validation*, single one-study, and do not change the total number of independent direct-contact/parentage publications verified (currently one).
