# RHP001: Original wild Oenothera maternal-family heldout paternity prediction — unresolved treatment increment

**19 Nov 2026. Source-verifiable, pre-outcome source/grain and model locked; one independent original wild-plant research programme.** Empirical EGWEE only, **not** independent confirmation of direct contact/father-identity PR #90 and not a new rediscovery of already published pollinator-identity effects.

## Original data provenance and biological unit

Rhodes, Fant & Skogen (2017), *Pollinator identity and spatial isolation influence multiple paternity in an annual plant*, *Molecular Ecology*, DOI [10.1111/mec.14115](https://doi.org/10.1111/mec.14115), original Dryad [10.5061/dryad.p24q3](https://doi.org/10.5061/dryad.p24q3), identical official public [Zenodo original-source mirror 4942351](https://zenodo.org/records/4942351), CC0. The author deposited `multiplePaternity.csv`, published source **MD5 `600f6f370ffa8ad205d0ccb6bc92ab65`**. The exact file source bytes and 60 first-row-schema-supported maternal seed-family/fruit records are verified by the author-mirror record. Original population source matches:

- `plantID` = same maternal plant identifier across possible multiple fruit families, **23 independent maternal plant groups**, not 60 uncorrelated plants.
- `treatment` = original experiment `c` control, `de` day exclusion, `ne` night exclusion; **21, 20, 19** complete original fruit families, respectively.
- `isolation20` = original distance-to-20-nearest-plant isolation statistic, not directly measured pollinator visit or assigned father identity.
- `correlatedPaternity` = original per-fruit MLTR estimator from microsatellite offspring. Higher values reflect greater paternity concentration (two offspring more likely to share a sire), **not** a literal count of fathers or viable seedling offspring.

Independent original source-only first-row/MD5 catalogue [CI 44513179110](https://github.com/zuizui0223/egwee/actions/runs/44513179110) verified **9/9 original archived files**, including 175 pollinator foraging bout rows and 406 per-seed pollen-dispersal distances, but **neither has mother–father visitation partner identifiers**. No fabricated join. A separate `--source-only` eligibility stage, before fitted response directions, verified exact 60 complete seed families, 23 source maternal groups and all three treatments, passing the fixed >=48 families, >=18 mothers, >=10/arm criteria.

## Original-source prospective model specification

[`RHP001_MATERNAL_HOLDOUT_FREEZE_20261119.md`](RHP001_MATERNAL_HOLDOUT_FREEZE_20261119.md) was committed **before inspecting any new signed correlated-paternity model results**. One original maternal group at a time was held out completely, ensuring that fruits from the same original mother never occur in both train and test.

- Mnull = mean original MLTR correlated paternity in the training fruit families.
- M0 = unpenalized-intercept ridge λ=1 with training-only z-scored `log1p(isolation20)`.
- M1 = same M0 plus original categorical day/night pollen access exclusion (`de`, `ne` dummy columns, `c` reference); all outcome units retained. Coded treatment is an intervention/availability, not an observed individual insect foraging visit.
- Heldout original fruit-family loss is aggregated **mother-equal**, avoiding pseudoreplication. 4,000 source whole-mother bootstrap resamples of already-scored heldout mother losses (seed 20261119; **no refitting**) assess the increment. Independently coded ridge normal equations and coordinate descent agreed <1e−8 under synthetic and original numeric verification.
- Predeclared bounded one-study support required M0−M1>0, whole-mother 95% bootstrap lower endpoint>0, **and ≥60% source mothers benefiting**. No post-result tuning, no exclusion of outlier mothers.

## Actual independent original-data heldout result

| Registered source mother-equal heldout metric | Source result |
|---|---:|
| Original complete source seed family / maternal groups | **60 / 23** |
| Mnull MSE | **0.12094457** |
| M0 isolation-only MSE | **0.09791388** |
| M1 isolation + visitor exclusion treatment MSE | **0.09057744** |
| **M0−M1** (positive would favor richer model) | **+0.00733644** |
| Relative MSE improvement versus M0 | **+7.49%** |
| Whole-mother bootstrap 95% interval for M0−M1 | **[−0.01199620, +0.02550438]** |
| Mother folds with positive M0−M1 | **14/23 = 60.9%** |
| Mnull−M0 MSE, descriptive | **+0.02303069** |
| Strict predeclared one-study decision | **`NO_RESOLVED_ONE_STUDY_TREATMENT_PREDICTION_GAIN`** |

Despite favorable point direction and 14/23 mothers benefiting, **the 4,000 maternal-bootstrap CI crosses zero**; the conjunction rule FAILS. This is **not** a biological equivalence test, evidence that pollinator identity does not affect plant mating, or disproof of the original authors' established near-twofold difference in number of sires. It merely says that this source model and out-of-mother prediction task have not demonstrated a robust incremental predictive benefit from treatment over spatial isolation.

[Executed source-original workflow run 44513859266](https://github.com/zuizui0223/egwee/actions/runs/44513859266) reported both the original outcome-blind 60/23/21+20+19 source grain and all heldout model scores with independent numerical solver controls, derivative artifacts only. Check the latest branch-head workflow status separately before any merge; the report intentionally does not mark this original negative/unresolved result as a submission-grade replication.

## Ecological interpretation, novelty and limits

The original 2017 authors **already** showed hawkmoth vs solitary-bee pollination identity affecting multiple paternity (average near twofold sire diversity) while plant spatial isolation also reduces diversity. EGWEE does not claim either as new. The incremental project-specific finding here is a **withheld-mother predictive assessment**, with modest but **uncertain** treatment signal beyond maternal isolation. A significant published group mean does not automatically imply reliable prediction of an unseen maternal plant's family-specific genetic output.

Comparison with PR #90 is useful for clarifying **measurement stages**, not for a quantitative two-study effect synthesis:

- PR #90: Barbot 2026 experiment, actual `mother × father` identified genotype paternity and inferred pollinator contact, +12.61 pp conditional on sampled mother/sire genetic offspring marginals at a frozen 10-flower carryover, and +11.70 pp in a posthoc deduplicated pair-weighting check, all **within one experimental research programme**.
- RHP001: Rhodes 2017 independent wild study, **maternal family** molecular correlated paternity plus exclusion treatment/isolation, **no available plant-specific visitation partner edge**; weak/uncertain out-of-mother treatment prediction.
- Leventhal 2026: another independent original study has four populations and genetic pedigrees/phenology, but its Dryad original file streams returned HTTP 401 here; metadata presence does not justify an invented original matched estimate.

No causal statement that the behavioral guild *information processing ability*, successful donor-specific pollen, compatible paternal genotype, or trait fitness was measured. The source pollinator bout table is not linked to each maternal family by individual observations; treatment exposure is not measured behavior. The original MLTR correlated-paternity output is a statistical genetic estimator, not direct compatible pollen receipt or offspring survival. Site/season variation cannot be generalized from one wild study or 23 mothers. No original genotype, individual mother identifiers, original phenotype values, infant genotypes, or raw observation rows have been redistributed.

## Next scientifically decisive independent panel

Acquire a second **truly independent source with both individually traced partner-specific pollinator contacts and a linked mother/father paternity ledger**, with source-authenticated effort and assigned parent confidence. Only then can PR #90's exact source-conditional contact→father identity null be replicated. For current available data, cross-programme claims should be expressed as **information sufficiency differs by observation stage** as a hypothesis, not a proven universal mating-translation principle.

No change to historical EGWEE natural fragmentation five-cluster analysis, original QPF source counts, the Barbot PR #90 effects, CropPol/EuPPollNet or theory egwe; this source analysis is an independent DRAFT PR on main.
