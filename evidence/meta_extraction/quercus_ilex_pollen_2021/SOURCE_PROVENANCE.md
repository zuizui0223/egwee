# Quercus ilex pollen-addition two-year experiment: original data provenance

Original peer-reviewed publication: Bogdziewicz et al. (2020), *Ecology Letters*, [doi:10.1111/ele.13609](https://doi.org/10.1111/ele.13609).

Primary dataset deposit: Bogdziewicz et al. (2021), [Dryad doi:10.5061/dryad.sn02v6x2b](https://doi.org/10.5061/dryad.sn02v6x2b); mirrored open file in [Zenodo record 5306693](https://zenodo.org/records/5306693/files/pollen_addition_results.csv?download=1). Dryad dataset API reports license **CC0 1.0**. Source file `pollen_addition_results.csv`, original Zenodo MD5 `9bb924a2d0739e78e6823f1df6878e6a`, 31,609 bytes, 960 semicolon-delimited shoot records in 80 trees (TreeID 62 absent), each measured in 2018 and 2019, 3 shoots per treatment/year. The corresponding paper states 81 marked trees; **data file has 80 distinct TreeIDs**, never silently rename 80 as 81.

Treatments: Control and Pollen-addition (haphazard branches located apart **within the same tree**, not randomized independent trees). Columns are flowers, acorns_june (before peak summer drought), acorns_final (after summer drought, September). Missing values are either `NA` or empty and cannot be zero-filled. Tree is the repeated independent biological unit; three shoots are nested in tree×year×treatment.

Each analysis reconstructs the published shoot counts; checks 0 ≤ final acorns ≤ June acorns ≤ flowers when jointly observed. For stage-specific rates require jointly known flowers/June/final, so denominators are matched between June and final; sensitivity requires all **three** complete shoots per branch-arm. A tree-year with only one arm is not used for a treatment comparison. The source does not contain a full flowering synchrony variable or local rainfall: do not invent them or attribute year difference mechanistically to drought.

Citable source-linked data are not new original EGWEE observations, not a fragmentation programme and not a new admission to frozen 5/8/16 study denominators. The 2020 original paper **already reports** the synchrony/pollen-limitation causal test; this work concerns cross-season attenuation and year-dependence conditional on the source design.
