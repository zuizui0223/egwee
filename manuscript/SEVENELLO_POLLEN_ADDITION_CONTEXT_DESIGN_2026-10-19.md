# Sevenello pollen-addition response across edge and local context

Status: exploratory design fixed before any new OP–OPSupp outcome calculation on 2026-10-19; execution blocked by source-file delivery errors. This is an extension of the ongoing egwee research draft, not a replacement for the frozen direct-I–F endpoint or an additional independent study programme.

## Ecological question

Does the difference between natural seed production at woodland edges and cores change when pollen is added? A secondary question is whether the within-quadrat seed increment from pollen addition varies with bare-ground cover or neighbourhood floral abundance. These questions distinguish the observed response to pollen addition from the earlier association between transect bee counts and open-pollinated seed production.

The source already reports species-specific pollen-limitation indices and SEMs linking landscape/local variables with open-pollinated seed production. Re-estimating an association with floral abundance is not a new ecological mechanism. The incremental contribution here would be a paired, untruncated seed-count contrast at the physical-reserve level, with all fixed species results retained.

## Fixed source and units

Source: Sevenello, Walker & Mayfield (2026), DOI [10.1007/s10980-026-02305-2](https://doi.org/10.1007/s10980-026-02305-2).
Data: [Figshare 31072189, version 1](https://api.figshare.com/v2/articles/31072189/versions/1), DOI [10.6084/m9.figshare.31072189](https://doi.org/10.6084/m9.figshare.31072189), CC BY 4.0.
The existing file manifest is `evidence/meta_extraction/phase2_cf01_sevenello_figshare_manifest_v1.json`.

- `landscape_seeds.csv`: file 61446289, 135336 bytes, MD5 `40caf98755786e32bec89fffd4b114f6`; 2080 plant records with `id_plot,species,site,crop_type,transect,plot,treat,flower_num,total_seeds`.
- `local_seeds.csv`: file 61026250, 21953 bytes, MD5 `10f0b07ff3ff17ca94dbabdfbcec404e`; 520 quadrats with `id_plot,ground_p,wood_p,leaf_p,grass_p,canopy_p,total_flower`.
- `landscape_bees.csv`: file 61026244, 1775 bytes, MD5 `b6cbdd11787f5ef5210fefcd502a29f5`; 20 transect bee records.
- Source README: file 61491790, 17265 bytes, MD5 `2d2b98764a07bfefc2897089ee3291ef`.

Four different plants in a quadrat receive OP, OPSupp, Bag, and BagSup treatments. This is not a within-plant before/after comparison. The paper says plants were “arbitrarily assigned”; strict randomization has not been established. Report observed responses to supplementation rather than an unconditional randomized causal effect.

Retain the existing primary species GORO, LARO and POAR. Their union spans **7 physical reserves** and **9 site × crop blocks**. Species-specific counts are GORO 5 reserves/6 edge–core blocks, LARO 6/8, and POAR 4/6. Two crop sides of one reserve do not add independent reserves; species sharing a reserve do not add independent studies. POGN remains outside the primary comparison because its edge and core sites are not consistently paired within reserve.

## Primary estimand, fixed before outcome access

For each quadrat with both endpoints observed, define

`D = total_seeds(OPSupp) - total_seeds(OP)`.

The unit is viable-looking seeds per plant as assessed in the source; viability is not a germination experiment. Retain zero and negative responses without truncation. Do not divide by OP, add pseudocounts, or remove responses below a selected threshold.

For each species separately:

1. Average D within each transect.
2. Subtract Core from Edge within the same physical reserve × crop block.
3. Where a reserve has two crop blocks, average its block contrasts, then give physical reserves equal weight.
4. Report the mean reserve-level contrast, the individual reserve values, a small-sample t interval, and a leave-one-reserve-out range as descriptive uncertainty/influence information. Do not treat individual quadrats as independent landscapes.
5. Present OP and OPSupp edge–core contrasts on the identical complete-pair sample beside the difference in differences. This makes the biological direction visible rather than reporting an interaction coefficient alone.

All three primary species must be reported; there is no species selection by sign or p-value. No common raw-seed effect is obtained by averaging species with different seed-count scales. Any formal testing must identify the three-species family and retain its complete results.

## Fixed secondary local-context comparisons

Keep these secondary to the reserve-level edge comparison:

- Paired D against bare-ground cover, per 10 percentage points.
- Paired D against log1p neighbourhood floral abundance.

Estimate species-specific slopes after removing species-specific transect intercepts. Show OP and OPSupp slopes on the same quadrat set. Uncertainty and influence must respect the physical reserve clusters; with 4–6 reserves per species, conventional cluster asymptotics are weak and must not be sold as precise generalization.

Do not replace bare ground with whichever of canopy, litter, wood, or grass produces the largest result. Those covariates remain descriptive context. Near-neighbour flowers can represent both pollinator competition and favourable growing conditions, so a floral slope alone cannot distinguish those pathways.

## Missingness and sensitivity rules

- Join local records to plants by validated `id_plot`; check metadata consistency and uniqueness of one plant per quadrat × treatment before analysis.
- Preserve the existing verified site aliases, including WA12427–WA12430, together with crop and transect.
- Missing seed counts are not zero. Report expected quadrats, observed OP/OPSupp counts, complete pairs, and missingness by species, reserve, crop and Edge/Core before reporting outcome contrasts.
- The primary outcome is total viable-looking seeds per plant, consistent with the existing F endpoint.
- For LARO and POAR only, seeds per observed flower may be reported as a separately labelled sensitivity on positive, observed flower counts. Flower number is a different denominator and may itself respond to plant condition; this does not replace the total-output result. GORO has no comparable flower count because of destructive dehiscence.
- Available-plant treatment means may be shown as a missingness sensitivity, explicitly distinguished from the primary complete-pair contrast.
- Bag and BagSup are not added to the primary estimand or used to select species after seeing results.
- No derived OP transect table or schema can reconstruct the missing OP–OPSupp quadrat pairs.

## Interpretation limits

A larger D at edges would show a larger observed seed response to added pollen at edges in this study. It would not establish the landscape-level causal effect of fragmentation.

Low OP and low OPSupp in the same local conditions would be compatible with a limitation that pollen addition alone does not remove. It would not identify water, nutrients, herbivory, pollen quality or a physiological mechanism. A near-zero D cannot establish resource limitation, pollination sufficiency or equivalence.

The paper's rendered PLi equation uses OP in the denominator while its stated range and exclusion rule are inconsistent with that expression. Do not reconstruct the original PLi by guessing the denominator; the raw-count paired difference is independently defined.

## Execution record, 2026-10-19 UTC

The public Figshare article and file metadata endpoints responded successfully and confirmed the listed sizes, checksums and licence. Actual file downloads from the supplied `ndownloader.figshare.com/files/{id}` URLs returned HTTP 500 with `UnknownException`, including retries with the official API redirect. The institutional Figshare entry points did not provide an accessible separate mirror.

**No new Sevenello treatment contrast or environmental slope has been calculated.** There is no imputed result and no change to the 5-programme primary, 8-programme matched-I–F, or 16-programme broader evidence denominators. Wandoo's source-accessible reproductive-stage comparison proceeds separately. This design can be executed when the checksum-matching raw files become available.

