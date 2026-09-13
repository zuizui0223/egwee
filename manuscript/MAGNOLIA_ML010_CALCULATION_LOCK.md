# ML010 Magnolia calculation lock

Frozen after schema-only inspection and before numeric supplement rows were opened.

The supplement schema contains `Sink population of pollen`, `Population size`, `N`, source-population pollen percentages and `Total pollen immigrate (%)`.

## Common frame and exposure
Use exactly Y/T/A/B/C/F. Let `S_j` be the supplement population-size value only if it is verified to be the paper's source-defined summed adult-genet basal area. Primary fragmentation severity is `X_j=-z(S_j)` on the native source scale; no log transform and no substitution with adult-genet counts.

## C endpoint
With sink offspring count `N_i` and source-j pollen percentage `P_ij`, reconstruct `A_ij=N_i*P_ij/100`. For donor j, `cross_j=sum(i!=j) A_ij`, `total_j=sum(i) A_ij`, and `C_j=cross_j/total_j`. If source columns are ambiguous or any primary donor has total<=0, terminate rather than switching endpoints.

## F endpoint
`F_j` is the source Table 1 population mean seed-production rate (%) for the same six populations.

## Effects
Compute Pearson `r_C=cor(X,C)` and `r_F=cor(X,F)`, then Fisher z effects `atanh(r_C)` and `atanh(r_F)`. Negative effects mean lower support/function with stronger fragmentation severity; signs are not changed after opening.

## Dependence
Use a paired-population nonparametric bootstrap: seed 20260913, 10,000 resamples of six complete rows, require >=3 distinct populations and nonzero variance in X/C/F, symmetric clipping of |r| only at `1-1e-12` for atanh, and require >=8,000 valid replicates. The empirical 2x2 covariance of `(z_C,z_F)` is the working covariance matrix and must be finite and positive definite.

No analytic-variance substitution, zero covariance, alternate rank metric, subset deletion, alternate exposure or alternate endpoint is allowed after numeric rows are opened.
