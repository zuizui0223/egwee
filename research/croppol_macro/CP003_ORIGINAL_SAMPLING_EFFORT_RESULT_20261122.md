# CP003 — Source-verified CropPol sampling-effort bridge: very little new field-level effort

**22 November 2026.** Exact pinned original field **3,448 rows, 68 columns** and original source sampling **54,191 taxon × method rows, 12 columns**; file bytes verified by Git blob SHA1, byte length and published/source SHA256. Source original sampling SHA256: `aafba5d3dfbab2c93f3a60e31181d2c5b33535cc2c8f33b85495facb42382f30`. This audit examined source key and effort presence/distinctness only, **no outcome sign, coefficient, phenotype distribution, or predictive score**. [Source freeze](CP003_SAMPLING_EFFORT_JOIN_FREEZE_20261122.md), [executed derivative](CP003_SAFE_EXECUTED_RECEIPT_20261122.json), [CI 45009021317](https://github.com/zuizui0223/egwee/actions/runs/45009021317), [author source](https://github.com/ibartomeus/CropPol/tree/febec7dcc088ccf1bd721c41ce8dda87a2dcba1a/Final_Data).

## Identity and source grain

Original sampling rows represent taxon × method summaries, not one independent field or one census per row. Summing original `total_sampled_time` or `total_sampled_flowers` across taxon records would **artificially multiply sampling effort**. The source file has no separate sampling-year column; therefore the initial design blocked same study/site keys appearing twice in the field file rather than guessing a year.

**Executed source resolution:** all **3,448** field rows have distinct `study_id × site_id` pairs in this pinned version, so **0 field rows have the anticipated within-original-field-file ambiguous study/site join**. The sampling source has **2,578** distinct complete study/site pairs, of which **2,305** directly occur as field keys; **1,143** field rows lack a corresponding sampling key. This only proves string identity in this pinned compilation; it does not verify the biological survey period for a study labelled several years. There are **2** sampling source rows with missing/invalid taxon abundance, but those rows do not turn into zero visitor abundance.

## Actual strict visitor/direct production frame

The CP002 strict original 452 fields from 19 provisional source components remain **unchanged**; the sampling table matches 388 original field keys, fails to match 64, and 344 matched field keys contain multiple taxon records. A separate 120 matched keys have multiple/missing method labels under our strict rule, so source effort cannot be treated as single-method without more original protocol evidence.

| Source audit of 452 source-field records | Executed count |
| --- | ---: |
| Original field records with exact source sampling rows | **388** |
| Keys with one method and one repeated positive finite sampled time, no missing | **268** |
| Above with time exactly agreeing between source field and taxon sampling records | **194** |
| Above with **different** published source time values | **68** |
| Above with missing field time potentially fillable **without overwriting** the original source | **6** |
| Source keys with one method and unambiguous positive sampled area | **94** |
| Sampled area exact agreement with original field area-of-survey time-series | **88** |
| Source missing sampled area potentially recoverable from the sampling file | **6** |
| Sampled-flower count present as unique positive value under strict method requirement | **159** |

The **68 different time values are a provenance/measurement conflict flag**, not evidence of a corrupted study: the taxon-sampling file can combine methods and sampling effort differently from the original field's total or visitation-specific exposure. No source values are overwritten, summed or relabelled. Zero versus missing is preserved. Sampled flower number is a count of flowers within census visits, **not a standing floral-resource density measurement** and not an independently measured preharvest confounder.

## Strict area-normalized harvest mass

Among original CP002's **121** strict author-use-visits + `harvest_mass_area` fields from **five** provisional source components:

- **96/121** exact source study/site keys are represented among original sampling taxon rows; **25** have no sampling source rows.
- Only **8/121** retain one strict single-method, identical, positive source sampling time; all **8** already have an exactly agreeing positive field-level sampled time. **No additional missing time is recovered.**
- Only **8** retain a strict unique sampled-flower count, and **8** retain a strict unique sampled area. These are within the existing sample; they do not fill the missing **crop-field area** or **crop plant density** in the field table.
- Crucially the original **38/121** records with management + field area + plant density remain in **one** source component. The sampling taxon table contains neither `field_size` nor `plant_density`, so **it cannot rescue the CP002 three-covariate source-out model.**

## Whole-source quality descriptors

Across all 3,448 original field rows, the strict source effort audit found 2,305 sampling-matched keys; 1,143 unmatched keys; **40** possible new field-level sampled-time values and **11** possible sampled-area values under the no-disagreement/no-multi-method/no-partial constraint. It found **95** exact-key published time discrepancies in the full source. Those are flags for an author protocol reconciliation, not automatically data errors.

## Scientific admission

**`EFFORT_SOURCE_KEYS_AUDITED_NOT_MODEL_ADMISSION`.** The original source compilers described `total_sampled_time` in minutes, the total across repeated site surveys, while `total_sampled_flowers` is the sum of flowers inspected across censuses. Exact physical field/year visit accounting remains unverified. This join does **not** certify whether a field-level `visitation_rate` is derivable from the sampling table; we have not divided taxon abundance by survey time or generated adjusted visit rates.

The result is a useful *negative source-recovery finding*: new source rows are numerous, but the genuine increment in comparable **field-level** observation effort for strict production/visitation is tiny and **zero** for area-normalized harvest mass. Blindly adding 54,191 sampling rows to 3,448 field rows would manufacture pseudoreplicates and overconfidence.

A narrower **single-covariate source-out** rank forecast, using independently observed field size and exact source block keys, can be investigated as a separate **explicitly exploratory** reduced-context comparison; it cannot substitute field area for missing standing flower density, plant resources or source management effects. Even a favorable result is **not** a causal crop pollination benefit. Prior Reilly, Vezzani and other CropPol pooled yield associations remain prior art. No source row, site name, individual contact or numerical phenotype was redistributed. PR94 remains draft; no changes to `main` or theory `egwe`.
