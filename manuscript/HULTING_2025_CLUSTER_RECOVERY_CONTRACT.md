# ML007 / PS014 Hulting 2025 cluster-recovery contract

## Goal

Test whether Hulting et al. (2025), *Journal of Ecology* 113:531–541, DOI `10.1111/1365-2745.14452`, can provide a fourth independent multilayer fragmentation cluster from the replicated Savannah River fragmentation experiment.

Target layers:

- `I_interaction`: pollination rate;
- `F_reproductive_function`: total seed production per reproductive plant.

Flowering responses are retained as a mechanistic D layer but are not required for I/F cluster admission.

## Independent-unit structure

The experiment has 8 blocks, with 4 focal patches per block and patch-corner / plant observations nested below them. Species are measured in the same experimental landscape and therefore cannot be counted as five independent fragmentation studies.

Primary cluster unit = one study-level experimental cluster (`ML007`).

Within ML007 retain five species-specific I/F response pairs as dependent outcomes sharing blocks/patches:

- *Anthaenantia villosa*;
- *Aristida beyrichiana*;
- *Sorghastrum secundum*;
- *Carphephorus bellidifolius*;
- *Liatris laevigata*.

Plant rows, flowering structures, flowers, seeds, patch corners, and species outcomes do not become independent meta-analytic clusters.

## Locked common fragmentation exposure

Primary exposure = within-patch distance from the nearest habitat edge, in metres.

For common orientation define

`edge_severity = -z(distance_from_edge)`

where distance is standardized across the analysis frame before model fitting. Larger `edge_severity` therefore means closer to a forest edge / stronger edge exposure.

This exposure is fixed before raw outcomes are opened because the paper reports it for flowering, pollination and seed production in the same planted individuals and identifies edge proximity as the consistent fragmentation component affecting reproductive output.

Patch connectivity / patch type and edge-to-area ratio remain prespecified adjustment / sensitivity terms from the source models. They cannot replace edge distance as the primary exposure after outcomes are inspected.

## Locked I endpoint

Primary I endpoint = plant-level pollination rate used by the source: proportion of developed achenes/caryopses, corrected for pre-dispersal seed predation and averaged over collected flowering structures for each reproductive individual.

Primary analysis is species-specific and preserves the original hierarchical random-intercept structure:

`patch_corner nested in patch nested in block`.

Use the source beta-binomial model family / weighting where the raw representation permits exact recovery. Do not code the published nonsignificant edge result as zero.

## Locked F endpoint

Primary F endpoint = total seed production per reproductive plant, as defined by the source from mean developed seeds per structure multiplied by total flowering structures.

Use the source species-specific hurdle model representation. The primary cross-layer F quantity is the non-zero conditional seed-production response to edge severity because this is the component for which the paper reports the four-of-five species edge pattern. The zero/seed-occurrence component is retained separately as a prespecified sensitivity and is not substituted post hoc.

## Common effect representation

For each species and each layer, retain the edge-severity coefficient and its sampling variance/covariance from the source-equivalent hierarchical model. Orient effects so negative values mean deterioration under stronger edge exposure.

If model parameterization includes an edge-by-patch-type interaction, do not cherry-pick a reference-level slope. Derive one prespecified average marginal edge slope over the experimental patch-type distribution and propagate its covariance from the fitted model.

The primary ML007 object is therefore a dependent vector of up to 10 species-layer effects, not ten independent studies and not a simple unweighted species mean.

## Cross-layer dependence

Dependence must reflect shared blocks/patches/plants and shared experimental design. Preferred order:

1. source/model covariance if a joint representation is available;
2. fixed cluster/block bootstrap that resamples the 8 blocks and refits all species/layer models together;
3. if neither is reconstructable, retain species-specific effects descriptively but do not admit ML007 to covariance-aware synthesis.

Do not set cross-layer or cross-species covariance to zero by convenience.

If a block bootstrap is used, fix 10,000 resamples and RNG seed `20260913` before seeing the resulting covariance.

## Source opening order

1. inspect Dryad DOI `10.5061/dryad.bnzs7h4mb` metadata and filenames only;
2. inspect raw schemas / column names without outcome summaries;
3. verify that block, patch, patch corner, species, edge distance, plant size, pollination and seed variables are recoverable on compatible rows;
4. only then run all species I/F models in one fixed pipeline;
5. reconstruct dependence and test covariance admissibility.

## No-rescue rules

Do not:

- treat plant or seed rows as fragmentation replicates;
- count five species as five independent studies;
- code nonsignificant pollination effects as zero;
- drop *Liatris* because its F edge response is weaker;
- switch the primary exposure to patch type/connectivity after seeing outcomes;
- pool wind- and insect-pollinated species before species-specific effects are obtained;
- switch F from the non-zero hurdle component to the zero component because it gives a preferred result;
- ignore the edge-by-patch interaction if present;
- set covariance to zero;
- use figure digitization if exact raw/model data are available.

## Terminal outcomes

- `ML007_admitted_I_F_edge_covariance_aware`;
- `raw_hierarchy_not_reconstructable`;
- `source_model_not_reconstructable`;
- `cross_layer_covariance_not_reconstructable`;
- `source_access_blocked`.

All outcomes are acceptable.
