# Protocol amendment — effect units and pseudo-replication firewall

**Locked:** 2026-09-11, before quantitative synthesis and before any EGWEE meta-analytic effect estimate is admitted.

This amendment clarifies Section 5–6 of `META_ANALYSIS_PROTOCOL_2026-09-11.md`. It does not change the biological hypotheses, response layers, moderator set or sign orientation. It was triggered during source extraction for `PS001` (*Spondias purpurea*), when the publication exposed several summary-statistic denominators that are not interchangeable.

## 1. Experimental / observational unit controls the denominator

For a fragmentation contrast, `n` in a sampling variance must correspond to the independent unit at which the fragmentation condition varies or at which independent biological replicates are sampled for that endpoint.

Examples:

- if habitat condition varies among sites/populations, hundreds of seeds or individuals nested within a few sites do **not** become hundreds of independent fragmentation replicates;
- if a genetic-diversity table reports a mean across loci with SD across loci, the SD cannot be paired with the number of sampled individuals as though it were an individual-level SD;
- if paternity distances are measured for many offspring nested within maternal plants/sites, the offspring count is not automatically the independent `n` for the habitat contrast.

## 2. Hedges g admission rule

A two-group endpoint enters the primary Hedges-g stream only when all of the following are recoverable on compatible scales:

1. group means (or an exactly convertible contrast);
2. dispersion corresponding to the same observation unit as the mean;
3. independent or correctly clustered sample sizes for that dispersion;
4. the fragmentation/reference contrast and nesting structure.

If any item is missing, **do not manufacture g** from mismatched summary fields.

## 3. Model-based contrasts

When a paper reports a mixed-model/GLM habitat contrast with site/population nesting but does not expose compatible raw SD and independent n:

- retain the reported coefficient / estimated marginal means / test statistic and its SE/CI as a `model_contrast_pending_standardisation` record;
- do not convert it to Hedges g using individual counts from a lower hierarchical level;
- admit it to the primary effect stream only if a preregistered, mathematically valid conversion using the correct residual/cluster scale can be made before pooled outcome inspection.

Otherwise it remains descriptive/supporting evidence or enters a separately declared model-contrast sensitivity stream.

## 4. Genetic metrics

For `G_adult` and `G_offspring`, record explicitly:

- genetic statistic (`H_o`, `H_e`, allelic richness, inbreeding, etc.);
- unit over which the reported dispersion is calculated (locus, population, individual, bootstrap replicate);
- cohort;
- number of independent populations/sites per habitat;
- number of individuals and loci as separate fields.

Never use individual `N` with locus-level SD without a justified sampling-variance derivation.

## 5. Movement / paternity metrics

For pollen-flow distance, sire diversity and paternity metrics, record nesting separately:

`habitat -> site/population -> maternal plant/progeny array -> offspring/paternity event`.

A reported mean over paternity events is not treated as an independent-event habitat contrast unless the source analysis supports that level of independence. Prefer source model/site-level contrasts or a cluster-aware reanalysis when raw data are available.

## 6. Consequence for PS001 Spondias

The publication reports:

- fruit production and fruit set from trees nested in sites with site treated as a random factor;
- genetic diversity with individual sample counts but SDs reported for locus-level summary metrics;
- pollen-flow distance from assigned offspring nested within populations;
- paternity correlations/effective sire numbers from progeny arrays.

Therefore PS001 remains **priority extraction**, but no naive Hedges g is calculated from `N individuals/seeds` plus incompatible SEM/SD. Each endpoint must first receive an explicit `effect_unit_status`.

## 7. New extraction field

Every quantitative row must carry one of:

- `g_admissible`;
- `fisher_z_admissible`;
- `model_contrast_pending_standardisation`;
- `raw_reanalysis_required`;
- `descriptive_only`.

The reason is stored in `effect_unit_note`.

## 8. Firewall

This amendment is locked before pooled synthesis. It cannot later be relaxed selectively to admit an outcome because its sign or magnitude supports the hypothesis.