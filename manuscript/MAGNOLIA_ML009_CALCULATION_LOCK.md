# ML009 Magnolia calculation lock — frozen before supplement numeric rows

The electronic-supplement schema gate passed without printing numeric data rows. It confirmed one table containing `Sink population of pollen`, source `Population size`, maternal-sample `N`, source-population pollen percentages, and `Total pollen immigrate (%)`.

No numeric supplement row has been inspected when this calculation is frozen.

## Common population frame

Use exactly the six seed-sampled populations `Y,T,A,B,C,F`. Any D/E rows or columns are excluded from the primary paired cluster because no seed-production endpoint was sampled there.

## Exposure

For population j, `S_j` is the exact supplement `Population size`, interpreted according to the paper Methods as summed basal area (summed adult-genet size), not adult-genet count.

Primary fragmentation severity is

`X_j = -z(S_j)`

where z uses the six-population sample mean and sample SD. Thus larger X = smaller source-defined population support / stronger fragmentation severity. No log transform is used because the source female-reproduction model used population size on its native linear scale.

If the supplement `Population size` cannot be verified as the source-defined summed adult-genet size, terminate rather than substitute Figure-1 adult-genet counts.

## C: between-population pollen export

Let `N_i` be the supplement offspring count in sink population i and `P_ij` the supplement percentage of pollen assigned to source population j among offspring sampled in sink i.

Reconstruct observed donor-by-sink counts as

`A_ij = N_i * P_ij / 100`.

For each donor population j:

- `cross_j = sum_{i != j} A_ij`
- `total_j = sum_i A_ij`
- `C_j = cross_j / total_j`

`C_j` is therefore the fraction of the donor population's observed siring assigned to offspring in other populations, rather than raw total siring. This normalizes donor output by its observed total and avoids relabelling total male reproductive output as connectivity.

If any primary donor has `total_j <= 0`, or source-population columns cannot be mapped unambiguously to Y/T/A/B/C/F, terminate `C_population_vector_not_reconstructable`. Do not switch to `Total pollen immigrate (%)`, study-wide 6.09%, gamma, selfing, or raw siring counts.

## F: reproductive function

`F_j` is the source Table 1 population mean seed-production rate (%) for the same Y/T/A/B/C/F populations. No maternal-genet-level pseudo-replication is introduced.

## Primary paired effects

Compute Pearson correlations across the six populations:

- `r_C = cor(X, C)`
- `r_F = cor(X, F)`

and Fisher-z effects

- `z_C = atanh(r_C)`
- `z_F = atanh(r_F)`.

Because C and F are support/function outcomes and X increases with fragmentation severity, negative effects indicate deterioration with fragmentation. Do not reverse signs after observing results.

## Within-cluster covariance and uncertainty

Use a fixed paired-population nonparametric bootstrap:

- RNG seed `20260913`;
- 10,000 resamples of six population rows with replacement;
- resample the full paired `(S/C/F)` row so dependence is preserved;
- a replicate is valid only if it contains at least three distinct populations and nonzero variance in X, C, and F;
- calculate Pearson r and Fisher z in each valid replicate;
- correlations numerically equal to +/-1 are clipped only for `atanh` at `1 - 1e-12`, symmetrically and without reference to direction;
- require at least 8,000 valid replicates;
- the empirical 2x2 covariance of bootstrap `(z_C,z_F)` is the working sampling covariance matrix.

Require finite positive diagonal entries and a positive-definite 2x2 covariance matrix. Otherwise terminate `covariance_not_reconstructable`.

No analytic-variance substitution, zero covariance, alternative rank metric, log exposure, subset deletion, or alternate C/F endpoint is allowed after numeric rows are opened.

## Terminal decision

- all gates pass -> `ML009_admitted_C_F_covariance_aware`;
- source population-size semantics fail -> `source_population_size_values_not_recoverable`;
- donor export vector fails -> `C_population_vector_not_reconstructable`;
- paired frame fails -> `common_population_overlap_insufficient`;
- bootstrap covariance fails -> `covariance_not_reconstructable`.
