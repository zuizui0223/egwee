# Prospective natural joint-state discovery — *Eschscholzia californica*

## Purpose

This campaign asks whether a common measured ecological state can be synchronized across **pollinator availability, direct reproductive function, pollinator dependence/reproductive assurance, and mating outcome** in one field experiment.

The system is the June 2015 Hillesden estate experiment in Buckinghamshire, UK. Sixteen arrays were distributed across four 100-ha blocks; each array contained three experimental *Eschscholzia californica* plants, giving 48 focal plants. The arrays crossed florally rich and florally poor habitat and were used across a family of EIDC data products from the same larger experiment.

The target state is therefore closer to the natural condition map than a single interaction dataset:

`habitat / array context + pollinator availability/traits I,T + reproductive assurance R -> direct seed function F + mating/paternity G_mating/C`

## Source lock before schema inspection

Four EIDC datasets are fixed before any row-level outcome inspection:

1. **Pollinator availability / traits (`I/T`)** — DOI `10.5285/01906784-6742-44bf-b244-a4b63bed8d82`.
2. **Direct seed function / pollen limitation (`F_seed`)** — DOI `10.5285/8caf2d8a-564d-4f2e-a797-174165a83796`.
3. **Pollinator dependence / alternative route (`R`)** — DOI `10.5285/5b400b69-b828-45e8-b04e-7ccbfdb0987f`.
4. **Mating / paternity (`G_mating/C`)** — DOI `10.5285/7b721c07-bc38-4815-8669-4675867663d0`.

All four are NERC Environmental Information Data Centre products and are described as parts of the same larger field experiment.

## Schema-only boundary

Discovery may contain only source identifiers, hashes, archive members and header labels. It must not calculate or inspect outcome rows, values, frequencies, means, correlations, coefficients, p-values or effect directions.

## Fixed biological mapping target

From headers/keys only, the next stage may map source columns to experiment block/array, focal plant, habitat/context, pollinator taxon/count and ITD, exposed/supplemented seed function, exposed/excluded seed function, and selfed/outcrossed/paternity state.

## Prospective scientific question

> **After conditioning on measured pollinator availability/trait state, does floral habitat context become redundant for both direct reproductive function and mating outcome, or do reproductive assurance and mating connectivity retain distinct state information?**

This question is intentionally multi-endpoint. It does not assume that one sufficient state exists for every downstream process.

## Frozen identifiability rule

`joint_state_identifiable` requires common block/array identifiers across all four products, common focal-plant identifiers across the plant-level endpoint products, and habitat attachable by declared keys without reading values.

`partial_joint_state_identifiable` requires the common block/array hierarchy but allows at least one endpoint product to lack a common focal-plant key.

`not_identifiable_from_archive` applies if synchronization would require guessing IDs from row order, values, distributions, or post hoc combinations.

## Claim ceiling

Pan traps represent **pollinator availability/community state**, not direct visits to each focal plant. The campaign will not claim that floral-rich versus floral-poor habitat is itself a functional-fragmentation regime. Habitat context remains an upstream route whose residual predictive information is tested after measured process state.

## Stop rule

No seed-function variable, paternity variable, pollinator group, body-size metric, habitat contrast, spatial scale or join key may be selected because it gives a preferred result. If schema permits analysis, an exact second preregistration must specify the unit hierarchy, fixed model sequence, held-out validation and decision rules **before any outcome row is inspected**.
