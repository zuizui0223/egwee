# GloPL: original 2018 curated public dataset, mirrored unmodified for egwee research

Source: Bennett, J. M. et al. (2018), *GloPL, a global data base on pollen limitation of plant reproduction*, **Scientific Data** 5:180249, doi:10.1038/sdata.2018.249.

Dataset original: [Dryad 10.5061/dryad.dt437](https://doi.org/10.5061/dryad.dt437); **CC0 1.0** according to the Dryad API. GloPL compiles 2,969 pollen supplementation experiments from 927 publications spanning 1,265 plant species. Responses: FS (fruit set), SO (seeds per ovule), SPFR (seeds per existing fruit), SPFL (seeds per flower), and SPP (seeds per plant). Data from literature through 2015; not a contemporary census.

This **exact source CSV** was published by the dataset authors' project: [idiv-biodiversity/pollen-limitation-data-descriptor](https://github.com/idiv-biodiversity/pollen-limitation-data-descriptor/blob/abbe193770981b2c61713e75a0f01e004bdded8e/Data/GloPL_with_id.csv), source Git commit `abbe193770981b2c61713e75a0f01e004bdded8e`, Git blob SHA `d22fe333b19489c473e076dd173ed7a67b1afbf0`, original length **1,091,571 bytes**. No rows or columns modified, no sources re-coded. Python checker must validate exact Git blob SHA (Git object header + raw bytes) **before** numeric computations.

The source table contains one record per study-defined case; cases are not independent publications. Original authors already documented average pollen limitation, positive cross-endpoint correlations, endpoint priority order (SPP > SPFL > SPFR > FS > SO); these are not new EGWEE findings.

The purpose of this retrospective **egwee** audit is to cross-tab *signed treatment-mean contrasts for two outcome measures measured in the same GloPL experimental row* and check whether sign mismatch spans publications/families while preserving missingness, zeros and dependent study IDs. Do not equate 81 point-sign mismatches with 81 statistically demonstrated biological tradeoffs; shared-treatment covariance is unavailable. GloPL cases are **pollen supplementation experiments**, not independently sourced **fragmentation comparisons**. Therefore no registered frozen 5-cluster, 8 quantitative I-F or 16 broader fragmentation-programme denominators change.

Citation: Bennett et al. (2018), https://doi.org/10.1038/sdata.2018.249 and https://doi.org/10.5061/dryad.dt437. This source package preserves credit despite CC0 waiver.
