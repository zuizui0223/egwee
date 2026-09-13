# ML012 / *Dieffenbachia seguine* 2010 recovery result

## Terminal state

`population_specific_Nep_not_reconstructable`

ML012 is **not** admitted as a fourth covariance-aware cluster. The admissible cross-system denominator remains ML001–ML003.

## What was locked prospectively

Before exact population-level outcome values were used for synthesis, the recovery contract fixed:

- independent unit = population, with two fragmented populations (`F1`, `F2`) and two continuous populations (`C1`, `C2`);
- primary `C` = population-level pollen immigration fraction from the source assignment analysis;
- primary `G_mating` = the 2010 paper's effective number of pollen parents `N_ep` calculated from the adjusted `Phi''_ft` pollen-pool statistic;
- Hedges-g fragmented-minus-continuous representation with fragmentation n = 2 versus 2;
- a paired-population covariance proxy only if both exact four-population vectors were recovered;
- no substitution of mothers, offspring, loci, `r_p`, unadjusted `PhiFT`, effective pollination area, or adult-genetic observations after outcome access.

## C layer: exact population recovery succeeds

The programme thesis exposes the male-gamete assignment matrix for the same four populations. Its local-assignment diagonal is:

- F1 = 0.667
- F2 = 0.712
- C1 = 0.813
- C2 = 0.661

Therefore the population-level pollen-immigration fractions, defined prospectively as `1 - local assignment`, are:

- F1 = **0.333**
- F2 = **0.288**
- C1 = **0.187**
- C2 = **0.339**

The habitat means are 0.3105 for fragmented populations and 0.2630 for continuous populations. These reproduce the 2010 article's independent summary of approximately 31% immigration into fragments and 26% into continuous forest.

Using the repository's canonical small-sample binary contract (`J = 1 - 3/(4df-1)` and `metafor` LS sampling-variance semantics), the descriptive C contrast is:

- `g_C = +0.342450617324352`
- `V(g_C) = 1.01465905316323`

The positive sign means that the recovered assignment-based immigration fraction is, if anything, slightly higher in the two fragmented populations. This effect is retained only as descriptive recovered evidence because the companion primary layer fails its source-representation gate.

## G_mating layer: the locked adjusted N_ep vector is not source-recoverable

The 2010 Heredity paper explicitly states that its primary pollen-donor number is `N_ep` derived after correcting `Phi_ft` for parental inbreeding and selfing (`Phi''_ft`). It reports that the four adjusted values range from 1.0 to 2.4 and identifies C1 as having a high value, but the accessible indexed article representation does not expose the four Table 2 cells.

The 2006 thesis does expose an older population table with:

- F1: `PhiFT=0.377`, `N_ep=1.326`
- F2: `PhiFT=0.372`, `N_ep=1.344`
- C1: `PhiFT=0.340`, `N_ep=1.470`
- C2: `PhiFT=0.425`, `N_ep=1.176`

Those thesis `N_ep` values are explicitly calculated as the unadjusted `1/(2 PhiFT)` representation. Elsewhere the thesis also reports a distinct mating-system donor-number representation `1/r_p`. Neither is the prospectively locked 2010 adjusted `N_ep` endpoint.

Direct retrieval of the Nature PDF/Table 2 was attempted but did not yield a usable source representation in the current environment. The thesis PDF screenshot endpoint also returned a cache miss; text extraction nevertheless preserves the source tables above. No Table 2 cell was inferred from the reported range, a plotted point, or the adjustment formula.

## Why the cluster stops here

The recovery contract requires the exact same four populations for both C and G_mating before within-cluster dependence is estimated. Because the locked adjusted `N_ep` vector is unavailable:

- no G_mating Hedges g is calculated;
- no C/G covariance is calculated or set to zero;
- the exact C effect is not promoted by itself into the multilayer denominator;
- no switch is made to thesis unadjusted `N_ep`, `1/r_p`, `A_ep`, adult `H_O`, reproductive density, or another favorable endpoint.

This is a representation/source-recovery boundary, not evidence that donor diversity is unchanged by fragmentation.

## Reopen condition

Reopen ML012 only if the population-specific F1/F2/C1/C2 adjusted `N_ep` cells from the 2010 Table 2, or an author-supplied equivalent source table, become directly available. The existing C vector, G endpoint definition, 2+2 population frame, Hedges-g formula and covariance rules remain frozen.
