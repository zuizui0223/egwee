# CFTQ0018 / Zurich BetterBlooms gradient-recovery contract — 2026-09-24

## Audit status

Programme identity: `P2_CF01_ZURICH_2026`.

Linked sources:

- Reji Chacko et al. (2025), Data in Brief 62:112013, doi:10.1016/j.dib.2025.112013;
- Reji Chacko et al. (2026), Journal of Applied Ecology, doi:10.1111/1365-2664.70384;
- EnviDat raw dataset doi:10.16904/envidat.676;
- archived analysis code, BetterBlooms release `jae`, Git commit
  `d6361f6874398e797322afe07a8fea85a3c7e927`.

This is a **retrospective external recovery**. Numerical exposure and pollinator-count tables and
source-reported outcome direction were visible during source reconstruction before this contract was
committed. No prospective outcome-blind claim is made. Endpoint identities and aggregation rules are
fixed here before EGWEE effect calculation.

## Study geometry

The source experiment uses 24 Zurich home gardens as local habitat patches.

Landscape exposure is the source-defined proportion of built and paved surface within 500 m of the
garden centre, stored by the source analysis as `Urban_500`. The published methods define this from
the Zurich habitat-map field `versiegelu == versiegelt`.

Higher `Urban_500` = greater urban densification / habitat loss and therefore stronger
fragmentation severity for the registered gradient/generalisation stream.

Garden is the independent landscape unit. Plants, branches, umbels, flowers, fruits, pollinator
individuals, repeated capture windows and species observations are nested below garden and never
increase fragmentation n.

Garden 39 is excluded because every source analysis script removes it for insufficient sampling
effort. No additional garden is excluded unless the source's endpoint-specific analysis script
explicitly does so or the endpoint is genuinely missing.

## Locked I endpoint

For each phytometer species, primary I is the broadest source-defined direct visitor measure that is
available consistently across gardens:

`all-pollinator capture rate per 9 h`.

The source code calculates:

`daily_rate = A_allPollinators_<plant> / (sampling_effort_min_<plant> / 60 / 9)`.

The four phytometer mappings are:

- *Daucus carota* -> `A_allPollinators_Carrot`;
- *Raphanus sativus* -> `A_allPollinators_Radish`;
- *Onobrychis viciifolia* -> `A_allPollinators_Sainfoin`;
- *Symphytum officinale* -> `A_allPollinators_Comfrey`.

For *Symphytum*, the archived source table shows that the all-pollinator count is the same visitor
pool used by the source's Bombus-focused reproductive models; no taxon-specific alternative is
selected after effect calculation.

Pollinator richness and taxon-specific visitation remain sensitivity/descriptive endpoints.

## Locked F endpoint hierarchy

Use the first direct reproductive-success endpoint in the source habitat-analysis sequence for each
phytometer. This prevents selecting among fruit/seed endpoints after calculating fragmentation
effects.

### Daucus carota

Primary F = mean `n_seeds` per assayed umbel within garden, using rows available to the source
model after the source garden-39 exclusion.

### Raphanus sativus

Primary F = garden-level fruit set:

`sum(n_flowers_with_fruits) / sum(n_flowers_with_fruits + n_flowers_without_fruits)`.

Seed number per fruit is retained as sensitivity only.

### Onobrychis viciifolia

Primary F = garden-level fruit set using the same source restrictions as the published analysis:

- remove garden 39;
- require `n_inflorescences_assessed != 0`;
- remove gardens 19, 28 and 52 because the source script excludes them for insufficient scorable
  plants.

Within the retained rows:

`fruit_set = sum(n_flowers_with_fruits) / sum(n_flowers_with_fruits + n_flowers_without_fruits)`.

### Symphytum officinale

Primary F = garden-level fruit set:

`sum(n_flowers_with_seeds) / sum(n_flowers_with_seeds + n_flowers_without_seeds)`,

after the source garden-39 exclusion.

Seed set from ovule success is retained as sensitivity only.

## Common-frame rule

Each phytometer I–F pair is reconstructed on the exact intersection of gardens with:

1. source `Urban_500`;
2. the locked I endpoint;
3. the locked F endpoint;
4. all source-defined endpoint exclusions applied.

I is recalculated on that same garden subset before the paired gradient effects are constructed.

The four phytometers are repeated endpoint panels within one programme, not four independent
programmes.

## Gradient effect representation

This programme is not converted into a binary fragmented/reference comparison.

For each phytometer and layer:

1. retain source `Urban_500` unchanged as the fixed severity axis;
2. calculate Pearson `r` between `Urban_500` and the garden-level endpoint;
3. calculate `z = atanh(r)`;
4. use marginal Fisher-z variance `1/(n-3)`;
5. orient higher `Urban_500` as stronger fragmentation, so negative z means lower interaction or
   reproductive function with greater habitat loss.

No threshold on impervious surface is created.

## Within-phytometer dependence

For each I–F pair sharing the same gardens:

1. fit endpoint ~ intercept + `Urban_500` separately for I and F;
2. retain garden-level residual vectors;
3. calculate their Pearson residual correlation `rho_IF`;
4. set `Cov(z_I,z_F) = rho_IF * sqrt(V_I * V_F)`;
5. require the 2x2 working covariance block to be positive definite.

This is labelled an approximate reconstructed dependence proxy, consistent with the existing
gradient contract. Covariance is not set to zero to make the pair convenient.

## Programme-level interpretation

If the source rows and all four phytometer-specific calculations reproduce deterministically:

- effects are labelled `fisher_z_admissible`;
- the programme is labelled `gradient_generalisation_multilayer_cluster`;
- it contributes one programme identity only;
- it does **not** increment the primary Hedges-g I-F programme count;
- phytometer species are not treated as independent studies.

## No-rescue rules

Do not:

- replace `Urban_500` with another urbanisation variable;
- choose 50/100/250/500 m scale after comparing response results;
- dichotomize gardens into low/high urbanisation;
- select a pollinator taxon because it yields a stronger response;
- switch between fruit and seed endpoints because one is larger or more significant;
- use lower-level plant/flower/fruit/pollinator observations as landscape n;
- drop gardens because they weaken a correlation;
- treat the four phytometers as four independent programmes;
- convert these Fisher-z gradient effects to primary Hedges g.

## Terminal outcomes

- `zurich_gradient_IF_covariance_aware`;
- `garden_exposure_join_failed`;
- `phytometer_common_frame_insufficient`;
- `garden_level_F_not_reconstructable`;
- `gradient_covariance_not_positive_definite`.

All outcomes are retained.
