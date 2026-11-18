# Sevenello 2026 missingness amendment — 2026-09-25

## Trigger

The frozen recovery script opened the public response file only after the primary Edge/Core
estimand, I endpoint, F endpoint, species panels and effect rules were committed.

The first execution terminated **before any Hedges-g effect or covariance was calculated** because
some plant-level `total_seeds` cells are encoded as literal `NA`.

This amendment fixes missing-value handling before rerunning the effect calculation.

## Locked rule

For `landscape_seeds.csv`:

1. retain `treat == OP` exactly as frozen;
2. interpret blank or literal `NA` `total_seeds` as missing measurement, never as zero;
3. exclude only the missing plant row from the transect-level mean;
4. calculate `F_mean_total_seeds_OP` as the arithmetic mean of all non-missing OP
   `total_seeds` rows in that species x normalized-site x crop x transect;
5. retain the transect whenever at least one non-missing OP observation exists;
6. store both planned OP rows and non-missing OP rows for every recovered transect;
7. if an entire primary transect has no non-missing OP value, terminate
   `sevenello_primary_species_common_frame_mismatch` rather than impute or change the frame.

No arbitrary minimum-completeness threshold is introduced after seeing the missingness pattern.

## Prohibited rescue

Do not:

- code `NA` as zero seed production;
- replace the transect with another site;
- switch from total seed production to seeds per flower;
- remove a transect because its observed F value is extreme;
- promote POGN to primary if a primary transect fails;
- change the Edge/Core contrast.

This missingness amendment changes no biological endpoint, fragmentation estimand, species-panel
rule, independent-unit definition or dependence method.
