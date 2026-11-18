# Official Dryad file description vs ancillary 2014 temporal-sheet glossary

**Verified external primary archive description, 2026-11-18.** Official dataset: [Layman et al. Dryad 10.5061/dryad.2pj0j](https://datadryad.org/dataset/doi%3A10.5061/dryad.2pj0j). The dataset's text descriptions for **both** `Pollinator Data 2014` and `Pollinator Data 2015` say:

> `Ant` = ant; `Beetle` = beetle; **`B` = honeybee or carpenter bee**; **`L` = lepidoptera**; `F` = fly excluding bee-fly; **`BF` = bee-fly**; `AH` = Andrenidae/Halictidae; `K` = katydid; `U` = unknown.

This **official dataset-level codebook supersedes the assumption that the source's single ancillary temporal-sheet labels apply to every worksheet.** The directly observed 2014 `Landersville Field - Temporal` row-1 sheet still literally calls `Bf` bee-fly, `B` butterfly, `H` honey bee. These two descriptions **conflict** for `B`; the conflict is preserved rather than silently edited. We therefore use the published dataset-level glossary for the **main array** field codes and treat the temporal-sheet glossary as a sheet-specific note. Lowercase `Bf` has a literal bee-fly gloss in that temporal sheet but no explicit corresponding token on the Dryad dataset-page 2014 main-array code list; treating `Bf` as a bee-fly alias remains plausible but requires caution.

**What this resolves:** canonical main-array `BF` as bee-fly, `B` as honeybee/carpenter bee, `L` as lepidoptera. Prior LA004's `B=Butterfly` assertion is only valid as a literal **ancillary worksheet quote**, not as the default published array code. This correction is source-methodology only, not a reevaluation of any genotype/seed/visitation effect.

**What remains unproven:** the published 3,748 visitation numerator does not match the complete original event/position tally; 2014 `Bf`/uppercase `BF` grouping is not documented by a single preprocessing script; 17 published bagged controls do not map uniquely onto 21 source rows. There is no automatic inference of wrongdoing or source error, and no arbitrary inclusion or recoding selected to fit the published numbers.

All original LA001/LA002 seed-prediction negative decisions and LA005 predeclared lower-bound mating outcome analysis are kept separate. Source audit Issue #67 remains open.
