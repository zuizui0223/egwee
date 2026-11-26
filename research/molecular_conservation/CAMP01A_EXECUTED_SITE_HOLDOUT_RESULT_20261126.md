# CAMP01 / CAMP01A — independent Campanula experimental colonization dataset, executed site transfer result (2026-11-26)

**Decision: NO_SUPPORTED_SITE_TRANSFER_INCREMENT.** A completed source-amended within-programme holdout test, not a failed data access, not an independent confirmation of the EGWE model, and not a test of molecular S-locus compatibility.

Original publication: Makowski, Lamb & Galloway (2024), American Journal of Botany, DOI [10.1002/ajb2.16351](https://doi.org/10.1002/ajb2.16351); official CC BY 4.0 original datasets [10.5281/zenodo.10814705](https://doi.org/10.5281/zenodo.10814705). The original authors already showed that autonomous selfing buffered mate shortage in experimental colonization, and that visitation per flower did not track effective mating straightforwardly. Our narrower test asks whether observed visitation × source-population autonomy adds predictive information beyond the published experimental size × autonomy structure.

## Source and frozen stops
- Original protocol `03bc79ff02158e73e08138efcb5440130e6f22c0`. Initial run [45760327934](https://github.com/zuizui0223/egwee/actions/runs/45760327934) stopped on the source-native seednumber header; second run [45760409766](https://github.com/zuizui0223/egwee/actions/runs/45760409766) verified both file hashes but stopped on 56 pollinator records vs 53 published reproductive experimental populations.
- [Source-only alignment run 45760495519](https://github.com/zuizui0223/egwee/actions/runs/45760495519): 237 seed rows, 53 seed-side experimental population×site keys, 56 unique pollinator keys, 53 exact key joins, 10 sites, no design conflicts, 3 pollinator-only keys (2 low/single, 1 high/single), 2 matched start-date strings disagree, 128 plant keys and 109 with both C/S arm labels, 51 population keys contain paired labels. No seed or visitation association computed in the source-only audit.
- Original `PLdataindividual.csv` SHA256 `8a2a38a6552126273a83873e317ee68e1472231e19a8090436006736e30053c3` and `pollinator.csv` SHA256 `51101f4705b436cd75d21643910bb1fd611df4e71701918e0dcec24c07b009d5`, both pinned to originally verified published MD5 checksums.
- Source-only amendment `7d7d8a01ba051f291493f096a6c86d07a28dc428` freezes exact-date matching before any fitted seed–visitation association. The deposited treatment labels are C/S; their mapping to control/supplemented is not independently verified. The literal S−C paired log1p response reverses sign under label swapping, leaving ridge predictions' squared errors and the model-comparison gain identical. No biological direction is claimed.
- [Executed run 45760620127](https://github.com/zuizui0223/egwee/actions/runs/45760620127), aggregate artifact [15090006666](https://github.com/zuizui0223/egwee/actions/runs/45760620127/artifacts/15090006666), ZIP SHA256 `b0a12af73616e7e9892277dd9b8ab18c78260bd04d568d606f88a28002c565af`. No original individual rows or identifiers redistributed.

## Actual inclusion
53 reproductive population keys; 2 exact date-string mismatches excluded, 2 of the remaining 51 lack a paired plant, 9 further lack recorded visitation. Final **40 experimental populations in 10 repeatedly used sites**, four founding source populations. Date-matched groups before excluding missing visitation: 107 paired plants, 19 unpaired, 0 missing seed count records, 24 explicit zero-seed rows. These are not all plants in the final 40-population analysis. No missing visit values or pollinator-only seed outcomes imputed.

## Fixed model comparison
Each experimental population gets equal weight. Outcome = mean of individual within-plant coded S−C differences in log1p of within-arm mean seed count. Site holdout (all experimental populations at a site excluded together). Baseline M0: population source indicators, autonomy, single/small size, autonomy × size, training-standardized log1p(visits per flower). M1 adds autonomy × observed visitation. Ridge lambda=1, no tuning.

| Fold | N | M0 MSE | M1 MSE | M0−M1 |
|---:|---:|---:|---:|---:|
| 0 | 4 | 0.208345 | 0.281600 | −0.073254 |
| 1 | 5 | 2.135626 | 2.013987 | +0.121639 |
| 2 | 4 | 0.619036 | 0.917331 | −0.298295 |
| 3 | 5 | 0.809600 | 0.723749 | +0.085852 |
| 4 | 5 | 1.934607 | 2.577033 | −0.642426 |
| 5 | 4 | 0.873417 | 0.699192 | +0.174225 |
| 6 | 3 | 1.698419 | 1.458481 | +0.239938 |
| 7 | 4 | 0.936988 | 0.854922 | +0.082066 |
| 8 | 3 | 1.345315 | 1.150760 | +0.194555 |
| 9 | 3 | 2.614683 | 2.462706 | +0.151977 |
| **Pooled** | **40** | **1.2981390922** | **1.3200466265** | **−0.0219075343** |

7/10 sites improved, but pooled error increased **1.69%**. The fixed two-part success criterion requires positive pooled gain AND ≥70% site wins. It fails. Do not drop fold 4 or change visit measure, covariates, grouping, weighting, or outcome after this result. No p-value or causal conclusion.

## Scientific interpretation
- This does NOT reject the original paper's experimentally supported reproductive assurance/density-by-autonomy result. It rejects support for the specified additional visitation-by-autonomy predictive increment in these 40 complete paired experimental populations.
- Observed visits per flower are not compatible pollen or pollen-tube success. Autonomy labels derive from just four source populations and are not directly sequenced genetic states. Short-term seed production is not recruitment or realized population recovery. Selective missing visitation (9 groups), 2 unresolved date strings, 3 visitation-only groups, and unverified arm code mapping remain explicit limitations. This is within-experiment new-site prediction, not transfer to independent natural landscapes or a molecular G×I×F test.
- `Argentina anserina` 2024 QPF002 (10.1098/rspb.2023.1519) is already covered by the 2026-11-18 source gate; genomic Ne × visitation and pollen histology were reported by the original authors. Source grain across 2019–22 is not synchronized. Do not count its 2025 companion as independent. `Echinacea angustifolia` is a promising distinct programme for directly observed compatible mating/phenological overlap and paternity; primary Ison et al. (2014) assigned paternity to 832 of 927 seedlings from 37 maternal plants, but source-matched raw seed output and compatible-donor availability are not yet verified. Future independent acquisition must preserve these distinctions.
- LUPF1 source stop and LUPF2 exploratory phenology-to-seed proxy gain remain frozen. Current molecular conservation main question is still NOT IDENTIFIABLE from these sources. Preserve this negative result rather than seeking a favorable variant.
