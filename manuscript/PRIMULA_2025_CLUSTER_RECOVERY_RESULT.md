# ML006 / PS016 Primula 2025 recovery result

## Terminal state

`common_population_values_not_recoverable`

No common-exposure G/I/F effect was calculated.

## Prospectively locked design

Before population-level supplementary values were inspected, the recovery contract fixed:

- common landscape exposure: forest cover within 1000 m;
- common overlap: the 15 populations with pollinator surveys;
- G_adult primary endpoint: nucleotide diversity `Pi`;
- I_interaction primary endpoint: pollinator abundance per 30-min survey;
- F_reproductive_function primary endpoint: seed number per fruit;
- common response basis: `Y ~ forest1000_z + forest1000_z^2` for every layer.

The 1000 m scale was selected prospectively because the source F model uses quadratic forest cover at 1000 m and the source I candidate set explicitly evaluates the same 1000 m quadratic exposure. The better-fitting 750 m I model was not substituted.

## Supplement audit

The Elsevier supplement `1-s2.0-S0006320725000813-mmc1.docx` was downloaded directly and inspected in CI. It contains 12 tables.

Relevant source representations are:

- Supplemental Table A1: all 33 population identities plus habitat, region, population size, sampling counts, `Pi`, and `PP`;
- Supplemental Figure A2: map identifying the 15 pollinator-survey populations graphically;
- Supplemental Figures A3/A5: correlation graphics containing landscape/pollinator variables;
- Supplemental Table A9: fitted/model-selection representation for seed number per fruit versus landscape variables, including `f1000` and `f1000^2`, but not the exact population-level response/exposure table;
- Supplemental Table A10: pollinator visitor taxa and total individuals, not one pollinator-abundance value per focal population;
- Supplemental Table A11: fitted/model-selection representation for seed number per fruit in the 15-population pollinator subset;
- Supplemental Table A12: fitted/model-selection representation for pollinator abundance versus forest cover, including the 1000 m candidate, but not exact population-level values.

Thus the supplement does not expose one exact keyed table from which `forest1000`, `Pi`, pollinator abundance, and seed number per fruit can be joined for the same 15 population identities.

## Why no reconstruction was attempted

The missing values could only be approximated by digitizing maps/correlation figures or by combining fitted curves with separate tables. Both operations were forbidden prospectively because they would manufacture the common population frame rather than recover it.

The article states that the genetic sequence data are deposited under `PRJNA837403`, while the remaining datasets and R code used for the analyses are available from the corresponding author on reasonable request. The public sequence archive alone does not supply the exact landscape, pollinator and reproductive population table required for this cluster contract.

This is therefore a source-representation boundary, not a biological null and not evidence that forest cover is unrelated to genetic diversity.

## Reopen condition

Reopen ML006 only if the exact population-level analysis dataset or author-supplied equivalent becomes available. On reopening, retain the already-frozen forest1000 exposure, 15-population overlap, Pi/I/F endpoints and common quadratic basis. Do not replace them after inspecting outcomes.
