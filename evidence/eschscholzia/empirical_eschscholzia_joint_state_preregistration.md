# Prospective natural joint-state discovery — *Eschscholzia californica*

## Purpose

This campaign asks whether a common measured ecological state can be synchronized across **pollinator availability, direct reproductive function, pollinator dependence/reproductive assurance, and mating outcome** in one field experiment.

The system is the June 2015 Hillesden estate experiment in Buckinghamshire, UK. Sixteen arrays were distributed across four 100-ha blocks; each array contained three experimental *Eschscholzia californica* plants, giving 48 focal plants. The arrays crossed florally rich and florally poor habitat and were used across a family of EIDC data products from the same larger experiment.

The target state is therefore closer to the natural condition map than a single interaction dataset:

`habitat / array context + pollinator availability/traits I,T + reproductive assurance R -> direct seed function F + mating/paternity G_mating/C`

## Source lock before schema inspection

Four EIDC datasets are fixed before any row-level outcome inspection:

1. **Pollinator availability / traits (`I/T`)**  
   DOI `10.5285/01906784-6742-44bf-b244-a4b63bed8d82`  
   Title: *Pollinator data from pan traps located in habitats comprising different floral cover in Buckinghamshire, UK*.

2. **Direct seed function / pollen limitation (`F_seed`)**  
   DOI `10.5285/8caf2d8a-564d-4f2e-a797-174165a83796`  
   Title: *The seed set of supplemented and pollinator exposed flowers from Eschscholzia californica plants located within habitats comprising different floral cover*.

3. **Pollinator dependence / alternative route (`R`)**  
   DOI `10.5285/5b400b69-b828-45e8-b04e-7ccbfdb0987f`  
   Title: *The seed set of Eschscholzia californica plants introduced into habitats comprising different floral cover*; exposed and pollinator-excluded flowers are represented.

4. **Mating / paternity (`G_mating/C`)**  
   DOI `10.5285/7b721c07-bc38-4815-8669-4675867663d0`  
   Title: *Paternity of Eschscholzia californica plants introduced to habitats comprising different floral cover*.

All four are NERC Environmental Information Data Centre products and are described as parts of the same larger field experiment.

## Fixed access route for discovery

The first machine-access route is the EIDC data-package service:

`https://data-package.ceh.ac.uk/data/<dataset UUID>`

where the UUID is the DOI suffix. This is an access/schema gate, not an outcome analysis. Run `32734878637` showed that this route returns a small HTML landing document rather than the data payload directly. The second access adapter therefore reads only that landing document's `href` / form `action` attributes and follows every same-CEH link attached to the same UUID or an explicit CSV/ZIP/download route. Candidate selection is URL-structural and occurs without data-row inspection. Every verifiable CSV/ZIP candidate is retained rather than selecting among them by content.

## Schema-only boundary

The discovery artifact may contain only:

- DOI / dataset UUID / fixed package URL;
- HTTP content type and response size;
- SHA-256 of the returned package/file;
- member file names if an archive;
- per CSV: row-independent header labels only;
- no data rows, values, frequencies, means, correlations, coefficients, p-values or effect directions.

The discovery code must not calculate even descriptive outcome summaries.

## Fixed biological mapping target

From **headers/keys only**, the next stage may map source columns to:

- experiment block and array;
- focal plant identity where present;
- floral habitat/context;
- pollinator taxon/count and source-provided body-size/ITD trait (`I/T`);
- exposed and pollen-supplemented seed function (`F_seed` / pollen limitation);
- exposed and pollinator-excluded seed function (`R`, pollinator dependence / autonomous route);
- selfed/outcrossed status and/or assigned father/paternity (`G_mating/C`).

No new endpoint family may be selected from values after the schema is seen.

## Prospective scientific question

> **After conditioning on measured pollinator availability/trait state, does floral habitat context become redundant for both direct reproductive function and mating outcome, or do reproductive assurance and mating connectivity retain distinct state information?**

This question is intentionally multi-endpoint. It does not assume that one sufficient state exists for every downstream process.

## Frozen identifiability rule

The classification is determined from **column/key presence only**.

### `joint_state_identifiable`

Call this only if:

1. all four process products (`I/T`, `F_seed`, `R`, `G_mating/C`) expose a common experiment **block + array** identifier or an unambiguous header-level equivalent; **and**
2. both seed-function products and the paternity product expose a common focal-plant identifier or an unambiguous header-level equivalent, so plant-level outcomes can be nested under the same array; **and**
3. habitat/context is explicitly represented in the endpoint datasets or can be attached by the same declared block/array key without reading values.

The pollinator product need not have focal-plant identity because pan traps are array-level availability measurements; it must, however, attach to the exact array hierarchy.

### `partial_joint_state_identifiable`

Call this when:

1. all four products expose a common block/array hierarchy, so the same field arrays can be synchronized; but
2. at least one of `F_seed`, `R`, or `G_mating/C` lacks a common focal-plant key.

This permits only an explicitly hierarchical array-level or mixed-resolution second preregistration. Missing plant identity may not be reconstructed from row order, outcome values, or sample counts.

### `not_identifiable_from_archive`

Call this if:

- the four products do not expose a defensible common block/array key; or
- a required process product is absent; or
- synchronization would require guessing IDs from row order, values, distributions, or post hoc combinations.

Thus a common block/array key is the minimum admissible bridge; shared plant identity in the three plant-level endpoint products separates `joint` from `partial`.

All three outcomes are acceptable and may not be changed after outcome values are seen.

## Claim ceiling

Pan traps represent **pollinator availability/community state**, not direct visits to each focal plant. Even a successful later test must preserve that proxy boundary.

The campaign will not claim that floral-rich versus floral-poor habitat is itself a functional-fragmentation regime. Habitat context remains an upstream route whose residual predictive information is tested after measured process state.

## Stop rule

No seed-function variable, paternity variable, pollinator group, body-size metric, habitat contrast, spatial scale or join key may be selected because it gives a preferred result. If schema permits analysis, an exact second preregistration must specify the unit hierarchy, fixed model sequence, held-out validation and decision rules **before any outcome row is inspected**.
