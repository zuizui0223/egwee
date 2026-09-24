# CFTQ0084 / western-Europe configurational-heterogeneity I-F recovery contract — 2026-09-24

## Programme

Programme identity: `P2_CF01_HASS_WEUROPE_2018`.

Primary source: Hass et al. (2018), *Proceedings of the Royal Society B* 285:20172242,
doi:10.1098/rspb.2017.2242.

Public source material includes the article's electronic supplementary data (S3) and R code (S4),
registered under Figshare collection doi:10.6084/m9.figshare.c.3994269.

This is a retrospective external recovery. The paper's qualitative conclusions are public and
were visible during screening. The rules below are fixed before EGWEE calculates any effect.

## Sampling hierarchy

The source selected **94 independent 1-km² agricultural landscapes** in four western-European
regions/countries. Within those landscapes it sampled **229 focal fields**, with 1–3 fields per
landscape.

The fragmentation/configuration exposure is defined at the **landscape** level. Therefore:

- independent EGWEE unit = landscape;
- focal field, transect, survey, pan trap, radish plant, pod, seed and insect = nested observations;
- `n` for a Fisher-z effect is the number of common landscapes, never 229 fields.

Country/region remains a grouping/context variable; it does not increase independent landscape n.

## Locked exposure

Primary exposure = source-defined **field-border density**, the length of agricultural field borders
per crop area within each 1-km² landscape.

The source interprets higher field-border density as greater configurational heterogeneity and
smaller-scale agriculture. To retain the EGWEE orientation in which larger exposure means stronger
fragmentation/simplification, define before outcome calculation:

`fragmentation_severity = - field_border_density`.

No threshold or country-specific cut point is created. Crop diversity and semi-natural cover remain
covariates/context and are not substituted for the primary exposure after seeing results.

## Locked I endpoint

Primary I = **wild-bee abundance** from the source pollinator survey.

Use the source's field-level response after its stated pooling across transects/surveys and any
source-defined field exclusions. If S3 exposes lower-level rows instead, reproduce that source
aggregation first.

Because the exposure is landscape-level, construct one I value per landscape as the arithmetic mean
of the retained focal-field I values in that landscape. Do not sum fields when landscapes contain
different numbers of sampled fields.

Honeybee abundance, hoverfly abundance and species richness are secondary/descriptive endpoints and
cannot replace wild-bee abundance because they produce a larger effect.

## Locked F endpoint

Primary F = **mean radish seeds per pod** from the sentinel *Raphanus sativus* experiment, matching
the source's field-level seed-set response.

Construct one F value per landscape as the arithmetic mean of retained focal-field F values on the
same common landscape frame used for I.

Do not substitute total seed count, pod count, another reproductive endpoint or a model-selected
response after calculating the primary effect.

## Common-frame rule

The primary I-F pair uses only landscapes with:

1. source field-border density;
2. at least one retained focal-field wild-bee abundance value;
3. at least one retained focal-field radish seeds-per-pod value.

I and F are each aggregated to one value per landscape before the exposure correlation is computed.

The exact retained landscape count is determined mechanically from the source identifiers and
missingness, not from response direction.

## Gradient effect representation

This programme remains in the Fisher-z gradient/generalisation family.

For each layer:

1. compute Pearson `r` between `fragmentation_severity` and the landscape-level endpoint;
2. compute `z = atanh(r)`;
3. use marginal variance `1/(n_landscapes - 3)`;
4. negative z means lower biological support/function under stronger fragmentation/simplification.

Do not convert the programme to a binary Hedges-g contrast.

## I-F dependence

On the common landscape frame:

1. regress I and F separately on the locked fragmentation-severity axis;
2. retain landscape-level residuals;
3. calculate `rho_IF` between those residual vectors;
4. set `Cov(z_I,z_F) = rho_IF * sqrt(V_I * V_F)`;
5. require the 2x2 working covariance matrix to be positive definite.

The covariance is a reconstructed working proxy, not an exact analytic sampling covariance.

## Admission

Admit one `gradient_generalisation_multilayer_cluster` only if:

- S3/S4 expose a reproducible landscape identifier and field-to-landscape mapping;
- field-border density can be joined without outcome-derived recoding;
- the locked I and F responses can be reproduced at field level and aggregated to a common
  landscape frame;
- at least four independent common landscapes remain and the Fisher-z/covariance calculations are
  defined.

Admission is based on effect-unit validity, not significance.

## No-rescue rules

Do not:

- use 229 focal fields as independent n for a landscape-level exposure;
- use transects, surveys, traps, plants, pods, seeds or insects as fragmentation replicates;
- change field-border density to crop diversity or semi-natural cover because results are stronger;
- switch I from wild-bee abundance to richness, honeybees or hoverflies after seeing effects;
- select only countries with a stronger relationship;
- dichotomize field-border density;
- treat the pollen-analogue border experiment as an additional independent landscape programme;
- mix this Fisher-z programme into the primary direct Hedges-g denominator.

## Terminal outcomes

- `hass_gradient_IF_covariance_aware`;
- `hass_supplement_access_blocked`;
- `hass_landscape_identifier_not_recoverable`;
- `hass_common_landscape_IF_frame_insufficient`;
- `hass_covariance_not_positive_definite`.

All outcomes are retained.
