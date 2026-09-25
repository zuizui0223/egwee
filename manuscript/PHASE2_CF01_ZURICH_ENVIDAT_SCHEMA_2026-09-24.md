# CFTQ0018 Zurich EnviDat schema gate — 2026-09-24

## Source

Open EnviDat dataset: doi:10.16904/envidat.676, linked to Reji Chacko et al. (2025),
doi:10.1016/j.dib.2025.112013.

The archive is inspected at schema level only before numerical response extraction.

## Archive result

- archive bytes: **4995435**
- files found: **22**
- all expected repository files present: **yes**
- raw field workbook sheets: **1**
- explicit impervious-surface term found in schema/README: **no**
- pollination/reproductive response terms found in schema: **yes**

The repository contains separate site, raw field, visitation/trait, and six species-level
seed/fruit-set files. No response means, effect directions, correlations, p-values, or
fragmentation effects were calculated in this gate.

## Admission question

The next gate is structural:

1. identify the exact garden identifier shared across exposure, visitation and reproductive files;
2. identify the source 500-m impervious-surface field;
3. verify that each candidate species has a common garden frame for I and F;
4. keep garden as the independent landscape unit;
5. only then freeze one I endpoint and one F endpoint before calculating a gradient effect.

The EnviDat archive itself does not store the impervious-surface field. The linked frozen source-code
release does: BetterBlooms `jae` commit `d6361f6874398e797322afe07a8fea85a3c7e927`,
`raw_data/explanatory_variables.txt`, contains `Urban_500` for the exact same 24 garden IDs.

The exposure join is therefore **resolved without substituting another urbanisation variable**.

Next: reconstruct the locked garden-level F endpoints from the EnviDat raw files and calculate
Fisher-z I/F gradient effects on source-defined common garden frames.
