# Fresh ecological validation of interaction–function decoupling — preregistration 2026-09-27

## Status

This is a **future-only ecological validation programme**.

It is written after the current I–F direction census was observed. Therefore every programme already contained in the search universe through the frozen 2026-09-18 CF01 cutoff is treated as a **burned discovery system** for the hypotheses below.

No current Phase-1 or Phase-2 result is reclassified as confirmatory evidence.

## Discovery pattern that motivates the programme

The complete registered I–F census contains eight programmes:

- seven permit a registered within-programme I–F comparison;
- three resolve a mismatch;
- all three resolved mismatches have reproductive function more negative than interaction/pollen quantity;
- four are unresolved;
- one programme is not pair-testable because paired covariance cannot be reconstructed.

The resolved examples are *Eucalyptus wandoo*, *Cardiopetalum calophyllum* and the Kakamega *Acanthopale pubescens* programme.

This 3/3 direction is **motivation only**. It is not the validation dataset.

## Ecological hypothesis

### H1 — downstream reproductive bottleneck

In newly observed fragmented plant systems, a measured interaction-quantity layer can remain comparatively intact while reproductive function deteriorates when successful reproduction depends on processes downstream of raw interaction quantity, such as compatible pollen, mating opportunity, pollen quality or post-pollination filtering.

The primary ecological prediction is therefore not “pollinators decline under fragmentation.” It is:

> **F-dominant I–F decoupling should be concentrated in systems where the measured I endpoint quantifies interaction/pollen quantity but does not itself measure effective compatible mating.**

### H2 — effective-interaction measurements should recouple I and F

When I is measured as an effective interaction endpoint—e.g. compatible pollen receipt, realized paternity, successful pollen transfer or another source-validated measure that already incorporates mating quality—the I–F mismatch should be smaller than when I is a quantity-only endpoint such as visit frequency, pollinator abundance or total pollen tubes.

This is a representation hypothesis about ecology, not a claim that one proxy is universally superior.

### H3 — reproductive dependence should amplify quantity–function decoupling

Among quantity-only I measurements, F-dominant decoupling should be more likely or stronger where plants have high dependence on outcrossed/compatible pollen and little independently demonstrated autonomous reproductive assurance.

Self-compatibility alone is insufficient to code assurance.

## Fresh evidence universe

Confirmatory evidence may enter only through one of two lanes.

### Lane A — future literature

Eligible primary studies must have a publication/data-release date **after 2026-09-18** and must not be a reanalysis or duplicate report of a biological programme already present in the frozen search universe.

### Lane B — prospective synchronized field data

A new field programme must measure on the same population/site × flowering window:

1. fragmentation exposure fixed before reproductive outcomes are analysed;
2. one quantity-level interaction endpoint;
3. one effective-mating/quality endpoint when feasible;
4. reproductive function;
5. independent habitat/population units with valid replication.

A field programme known from the current search universe cannot become fresh confirmation merely because new raw rows are released later; such recovery remains external replication/sensitivity.

## Endpoint classes fixed before fresh outcomes

### Quantity-only I

Examples: pollinator abundance; visitation frequency/occurrence; total pollen grains or pollen tubes without compatibility information.

### Effective I / mating quality

Examples: compatible conspecific pollen; successful single-visit pollen deposition calibrated to fertilization; realized pollen-donor diversity or paternity-based effective pollen flow; experimentally validated quality-weighted interaction.

A metric is not promoted from quantity-only to effective because it predicts F well.

### F

Use the first source-defined direct reproductive-output endpoint meeting the programme contract (e.g. fruit set, seed set, viable seed production) according to a frozen source-specific hierarchy.

## Primary estimand

Within each fresh programme:

`Delta_IF = effect(I) - effect(F)`

with effects oriented so more negative means lower support/function under stronger fragmentation.

- direct fragmented/reference studies use the frozen Hedges-g family;
- continuous fragmentation studies use Fisher-z;
- **effect families are never pooled numerically**.

Positive `Delta_IF` means F is more negative than I.

## Primary confirmatory test

The first formal test is opened separately within an effect family only after **>=5 genuinely fresh independent programmes** with pair-testable I and F have accumulated.

For each effect family:

1. retain one programme contribution after its frozen within-programme multiplicity rule;
2. estimate the mean `Delta_IF` with uncertainty;
3. report leave-one-programme-out influence;
4. test H1 only if the quantity-only I subset contains >=5 programmes;
5. compare quantity-only versus effective-I classes only if each retained class has >=4 independent programmes.

No cross-family Fisher combination is used to manufacture the gate.

## Moderator variables frozen for fresh validation

Primary:

- `interaction_measurement_class`: `quantity_only | effective_mating_quality`;
- `autonomous_reproductive_assurance`: `measured_present | measured_absent | not_measured`;
- `outcrossing_dependence`: `source_supported_high | mixed_or_partial | unknown`;
- `pollination_specialisation`: `specialised | generalised | unknown`;
- `fragmentation_component`: source-defined area/isolation/edge/habitat amount/composite/design.

Secondary: woodiness/longevity; fragmentation age relative to generation time; pollination vector; biome/region.

Coding uses source biology independent of I–F effect direction.

## No-rescue rules

Do not:

- reuse Wandoo, Cardiopetalum, Kakamega, Chaco, Sevenello, Zurich, milkweed or Pritchard as fresh confirmation;
- classify a species as outcrossing-dependent because F happened to decline;
- infer autonomous assurance from self-compatibility alone;
- call visit frequency “effective interaction” because it predicts fruit set;
- change the F endpoint after observing which gives the strongest I–F mismatch;
- pool Hedges-g and Fisher-z deltas;
- add studies only until the fresh directional hypothesis becomes significant;
- treat unresolved or inaccessible systems as zero mismatch.

## Decision states

- `fresh_gate_not_reached`
- `fresh_quantity_IF_validation_open`
- `fresh_effective_vs_quantity_comparison_open`
- `fresh_F_dominant_decoupling_supported`
- `fresh_direction_not_supported`
- `fresh_result_influential_system_dependent`

All are publishable outcomes.

## Relationship to the current manuscript

The present Journal of Ecology manuscript remains an empirical discovery/synthesis paper. This future validation contract is not required to complete or submit it.

The current manuscript may motivate the downstream-bottleneck hypothesis but must label the 3/3 direction census as descriptive and post hoc.
