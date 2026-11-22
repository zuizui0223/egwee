# CP004 — Visits do not transfer field-yield rankings beyond a field-size-only baseline in this exploratory CropPol panel

**22 November 2026.** **Executed original pinned CropPol field data**, with [pre-outcome-target freeze](CP004_REDUCED_BASELINE_SOURCE_RANK_FREEZE_20261122.md), [frozen-source CI](https://github.com/zuizui0223/egwee/actions/runs/45009495412), [safe result receipt](CP004_SAFE_EXECUTED_RECEIPT_20261122.json). The predeclared bounded **source transfer** support rule was **NOT MET**. The observed increment is negative, and is reported rather than switching outcome families, baseline variables, or source sets to search for positives.

## What was tested, and why this is different from earlier work

Previous CP002 structural audit found that a joint field area+management+plant density baseline for area-specific harvested yield is available in only **38 original fields from ONE provisional source component**, so the full-context model cannot be transferred across studies in this release. CP003 confirmed that adding 54,191 taxon-by-method sampling rows does not fill field area or crop plant density and adds **zero** original site survey-time records for the 121-field harvest-mass subset.

We therefore preregistered **a deliberately reduced-context, exploratory analysis**, to test not causal effects but whether recorded total visitor rate adds **out-of-source within-block ordinal production prediction** above field area, a weak but measurable baseline. This is not a replacement for the full-context question; no claim of identifying pollinator effects controlling crop resources, floral density, management, soil, pests, crop phenology or climate.

**Original source:** [author's CropPol v2.1.0 field file](https://github.com/ibartomeus/CropPol/blob/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Final_Data/CropPol_field_level_data.csv), exact author Git commit `febec7dcc088ccf1bd721c41ce8dda87a2dcba1a`, Git blob SHA1 `cd19a354741ac40428e6b94aa1ec2ee596ff0547`, original SHA256 `ecfa84d1f6a52f24f13b7096347a59f231e8cc77eef8692b0a0183ceca86f879`. No original source rows, IDs, field coordinates, outcomes or visitor values redistributed.

## Frozen eligibility and model

Original CP002 review supplies **452** fields with a direct primary output label, numerical valid total visitation, explicit timed focal/transect observation, known taxonomic survey scope and author `use visits` selector. Within `source component × crop × year × exact outcome-unit label × visit-unit label × observation method × taxa scope` comparison blocks, preselect at least **five unique fields** and **variation in field_size** in hectares. This predictor-only preflight gave **201 original fields, 12 blocks, 10 provisional source components**, identical to CP002 published counts; all 12 blocks also had some original visit-rate variation (not used as an exclusion).

Each field's outcome is ordered against other fields **in the same block**. The outcome `yield` is never numerically pooled across kg/ha and fruit/set counts. For each pair, predictor midrank differences for `field_size` and `visitation_rate` have consistent scale across blocks. No held-out source outcome mean, SD, or maximum is used to transform either predictor or target. This is **transductive ranking** of a set of fields for which their field-size and visit-rate predictors are known.

- **M0:** Ridge `lambda=0.10`, pairwise field-size rank difference only.
- **M1:** Identical M0 plus pairwise total visitation rank difference; no tuning.
- Hold out **one entire provisional original source component** at a time, train on the other nine; training gives equal weight to each source, equal weight to its eligible blocks, and equal weight to pairs in each block.
- Score concordance of predicted higher/lower `yield` for within-block pairs; ties in prediction receive **0.5**; ties in output are excluded but **counted**. Predictors are ranked within blocks from predictors only, including test covariates; test outcomes do not enter training ranks.
- Aggregate per block then per source then **ten-source equal**. Fixed `random.Random(20261122)` **4,000** complete-source bootstrap reuses per-source heldout losses; this is not a confidence interval over externally verified independent experiments.
- Predeclared support rule requires ≥8 source components scoreable, mean Δ>0, source-bootstrap 95% lower bound >0 and ≥70% scored components Δ>0.

## Verified original outcome

| Source-locked predictive quantity | Actual |
| --- | ---: |
| Source original direct/timed/author-use-visit field candidates | **452** |
| Eligible field-size-varying fields / homogeneous blocks | **201 / 12** |
| Provisional source components evaluated | **10 / 10** |
| Original outcome-discordant field pairs scored | **1,758** |
| Original outcome-tied field pairs excluded | **23** |
| **M0 source-equal pairwise ranking concordance** | **0.52398933** |
| **M1 source-equal pairwise ranking concordance** | **0.48603906** |
| **M1−M0 rank agreement increment** | **−0.03795027** (−3.80 percentage points) |
| 4,000-source bootstrap 95% interval for source-equal Δ | **[−0.06900665, −0.00806663]** |
| Heldout source groups better / worse / equal with visits | **3 / 7 / 0** |
| Visit rank ridge coefficient positive in fitted training models | **9/10** |
| Frozen bounded positive rule | **FAIL — `NO_RESOLVED_REDUCED_BASELINE_TRANSFER_GAIN`** |

Interpretation: a visitation rank coefficient trained in other source campaigns was usually positive, yet its additional prediction **failed to transport** in most withheld sources, reducing the prespecified source-equal yield-rank concordance. It is evidence that simply appending total visits to this weak field-size model **does not improve** heldout ranking in this selected original CropPol panel, not evidence that insects do not pollinate crops.

The evaluated 1,758 field pairs share field members; only the ten provisional source components are resampled. The percentile interval can be anti-conservative if the provenance graph misses shared source campaigns, and it does not address unmeasured confounding or source selection. Models are observational and rank-only, **not absolute forecasts of yield, yield increases, seed survival or pollination limitation**.

## Prior art and significance

CropPol is an established database, with earlier pooled visitor-yield results in [Reilly et al. (2024)](https://doi.org/10.1111/geb.13843), [Turo et al. (2024)](https://doi.org/10.1038/s41559-024-02460-2), [Vezzani et al. (2025)](https://doi.org/10.1111/1365-2664.70042). There is also prior cross-author heldout **visitation** prediction. No claim of first discovery of pollinator-yield heterogeneity or first source-heldout learning is made.

This result emphasizes a **measurement-scale / predictive-transport problem**, not a new universal ecological mechanism: a broad visitor count can contain genuine pollination information, but its relationship to production need not be transferrable across differently managed and measured crop systems under this limited baseline. Existing PR #90 genetic Brassica evidence that individual contacts discriminate genotyped sires under a parent-degree-preserving null is a different biological stage, cannot be meta-pooled or causally contrasted with this crop result.

The next defensible advance is an independently documented **preharvest resource/flower density/field management predictor** to make a substantive biological baseline in multiple source components. CP003 shows the published sampling taxon table alone does not add that. It would be inappropriate to choose an unregistered weaker baseline or a favorable crop subset after observing the negative result.

**Outcome claim status: exploratory negative incremental source-transferred predictive result, fixed before the numerical score but after prior CropPol publications and earlier EGWEE source analyses. Not a confirmatory source-independent test.** The historical stronger 3-covariate question remains **not estimable**. Draft PR #94, no merge to `main` or theoretical `egwe`.
