# Synchronized ecological field module for quantity–function decoupling — v1

## Goal

Prospectively distinguish two explanations for apparent interaction–function decoupling under habitat fragmentation:

1. **quantity bottleneck:** fragmentation reduces pollinator visitation / pollen arrival and reproduction follows;
2. **quality/mating bottleneck:** interaction quantity remains comparatively intact, but compatible mating or effective pollen transfer deteriorates before fruit/seed production.

The field module is designed for new systems only and is compatible with the fresh-validation preregistration dated 2026-09-27.

## Biological chain

Measure three linked stages on the same ecological units and flowering window:

```
I_quantity  →  I_effective / mating quality  →  F_reproductive
```

The central prediction for a downstream reproductive bottleneck is:

- fragmentation effect on `I_quantity` is weak or buffered;
- fragmentation effect on `I_effective` is more negative;
- fragmentation effect on `F` is similarly or more negative.

## Independent unit

Primary independent unit = **population / habitat patch / site**, whichever is the source-defined fragmentation unit.

Plants, flowers, visits, pollen grains, fruits, seeds, offspring and loci are nested measurements. They improve precision inside a site but never increase fragmentation `n`.

A fresh field programme should span a response-free fragmentation gradient or a predeclared fragmented/reference contrast with repeated independent habitat units.

## Exposure block — frozen before response inspection

Record source-relevant landscape structure:

- habitat area;
- isolation / nearest suitable habitat / connectivity;
- edge exposure;
- habitat amount in fixed radii where biologically justified;
- fragmentation age if independently known.

Choose the primary exposure before opening reproductive outcomes.

If multiple landscape metrics are needed, define a response-free composite from the landscape variables alone. Do not select the metric/radius that maximizes the I–F difference.

## Stage 1 — interaction quantity (`I_quantity`)

At each independent site measure at least one prespecified quantity endpoint.

Preferred hierarchy:

1. visits contacting reproductive organs per flower-hour;
2. total conspecific pollen deposition per stigma;
3. pollen tubes reaching the style/ovary;
4. total pollinator visitation/occurrence if contact cannot be resolved.

Observation effort must be standardized by flower availability and time.

Automated cameras may supplement direct observation, but machine detections are nested below site.

## Stage 2 — effective interaction / mating quality (`I_effective`)

At least one quality-sensitive endpoint is strongly preferred.

Options, in priority order where feasible:

1. compatible conspecific pollen grains / pollen tubes;
2. donor diversity or realized paternity from offspring;
3. outcross pollen-flow contribution;
4. experimentally calibrated single-visit effective pollen deposition;
5. source-validated quality-weighted interaction index.

Do not derive quality weights from the same F endpoint being predicted.

### Minimal mating-quality experiment

On a prespecified subset of maternal plants within every site, apply:

- open pollination;
- autonomous bagging;
- hand self-pollination when biologically meaningful and permitted;
- hand cross-pollination / pollen supplementation.

Use this to identify autonomous reproductive assurance, self-incompatibility/compatibility and pollen quantity versus quality limitation.

Treatment plants are nested within site.

## Stage 3 — reproductive function (`F`)

Primary endpoint hierarchy must be frozen before outcomes:

1. viable seed production per flower/ovule;
2. seed set;
3. fruit set;
4. another direct source-defined reproductive output if earlier stages are structurally unavailable.

Where feasible, retain fruit set and viable seed production together as dependent F endpoints rather than selecting the stronger response.

## Essential ecological covariates

Measure without using them to redefine fragmentation after outcomes:

- floral display / flower density;
- conspecific adult density;
- flowering phenology;
- plant size or resource state;
- pollinator community composition;
- local vegetation/resource context;
- weather during observation.

These are mechanism/context covariates, not replacement fragmentation exposures.

## Primary within-programme contrasts

For each endpoint, estimate the oriented fragmentation response with the programme's frozen effect family.

Define:

`Delta_QF = effect(I_quantity) - effect(F)`

`Delta_QE = effect(I_quantity) - effect(I_effective)`

`Delta_EF = effect(I_effective) - effect(F)`

Positive values mean reproductive function is more negatively affected than the interaction metric.

### Primary mechanism prediction

If effective mating is the missing bottleneck behind quantity–function decoupling:

1. `Delta_QF > 0`;
2. `Delta_QE > 0` is the primary localization prediction: effective mating deteriorates more than raw interaction quantity;
3. the sign of `Delta_EF` distinguishes downstream geometry:
   - near zero: F tracks effective mating;
   - negative: effective mating deteriorates more strongly than F, consistent with downstream compensation;
   - positive: F deteriorates more strongly than effective mating, consistent with a later post-mating/post-pollination filter.

The fresh H2 test therefore localizes the bottleneck rather than requiring exact recoupling. It is tested only when the same independent sites support all required endpoints.

## Site-level representation

Construct one analysis value per independent site and endpoint using a frozen aggregation rule.

Examples:

- mean contact visits per flower-hour;
- compatible pollen per sampled stigma;
- site-level paternity/donor-diversity statistic;
- site-level viable seeds per flower.

Within-site uncertainty can be retained hierarchically, but lower-level rows do not become fragmentation replicates.

## Replication and opening rule

The field programme itself may report its within-system ecological result at any defensible site sample size.

It counts toward the **fresh cross-programme validation gate** only if:

- independent fragmentation units are replicated;
- I quantity and F share the same sites/exposure window;
- dependence can be estimated or a prespecified hierarchical model supplies the joint uncertainty;
- no endpoint/exposure was switched after viewing direction.

The cross-programme confirmatory analysis remains closed until the fresh-validation contract reaches its independent-programme gate.

## Mechanism decision states

Within a field programme:

- `coupled_quantity_and_function`
- `quantity_function_decoupling_quality_recouples`
- `quantity_function_decoupling_quality_also_buffered`
- `interaction_decline_without_function_decline`
- `all_stages_decline`
- `mechanism_not_identifiable`

These are descriptive biological states, not labels selected from p-values alone.

## Strongest evidence for a downstream bottleneck

A programme provides strong support when the same fragmented sites show:

1. little loss of `I_quantity`;
2. reduced compatible-pollen / effective-mating measure;
3. reduced F;
4. pollen supplementation or cross-pollination partially rescues F.

This directly separates “pollinators are absent” from “pollinators are present but effective reproduction is constrained.”

## No-rescue rules

Do not:

- choose a landscape radius because it maximizes decoupling;
- replace total visits with a particular guild after seeing F;
- estimate pollinator-effectiveness weights from F;
- promote plants/flowers/fruits/offspring to independent fragmentation units;
- define autonomous assurance from self-compatibility alone;
- select fruit set versus seed set after seeing which is stronger;
- discard a site because its I and F directions are inconvenient;
- merge different flowering years unless the temporal pooling rule was frozen first.

## Deliverables

A complete programme should archive:

- site/exposure table;
- observation-effort table;
- quantity-level interaction summary;
- effective-mating/quality summary;
- reproductive-function summary;
- mating/pollen-supplementation treatment summary;
- site-level dependence representation;
- frozen analysis script and endpoint/exposure manifest.

## Relation to the current synthesis

This field module operationalizes the ecological hypothesis generated by the present discovery corpus. It is not required for the current Journal of Ecology manuscript and does not retroactively upgrade the current 3/3 directional census to confirmatory evidence.
