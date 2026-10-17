# SF05-93 / Parkia biglobosa Phase-2 recovery contract

**Locked:** 2026-09-19 before Parkia effect calculation is added to EGWEE.

## Goal

Test whether Lompo et al. 2020 can contribute a same-system Phase-2 multilayer fragmentation cluster using the paper's four independent Parkia biglobosa populations.

This recovery is information-driven. It is not used to repair the frozen five-cluster Fisher result and it does not change the Phase-1 baseline unless the separate Phase-2 promotion gate is eventually met.

## Fragmentation exposure and independent unit

Primary independent unit = **population**.

The source prospectively defines two higher-fragmentation cotton populations and two lower-fragmentation non-cotton populations:

- fragmented / higher-fragmentation: Walley, Vouza;
- reference / lower-fragmentation: Saki, Cassou.

The primary direct effect stream is therefore the existing EGWEE Hedges-g convention for `fragmented - reference`, with `n_fragmented = 2` and `n_reference = 2`.

Adult trees, maternal trees, embryos, seedlings, microsatellite loci and pollination events are nested observations. They do not increase fragmentation-level n.

Do not replace the source cotton/non-cotton contrast after outcome inspection with population density, plot area, pairwise tree distance, individual population rank or another predictor.

## Locked primary layers and endpoints

### G_adult

Primary G_adult endpoint = population-level **expected heterozygosity H_E of the large-tree cohort**.

Rationale fixed independently of the observed values:

- H_E is the existing primary genetic-state metric used in EGWEE recovery contracts where population-level microsatellite genetic state is reconstructed;
- large trees are the clearest adult/historical cohort in the source's cohort table;
- small-tree H_E is retained only as a prespecified cohort sensitivity and cannot replace the large-tree endpoint because its contrast is more convenient.

Orientation multiplier = `+1`: larger H_E means greater genetic support.

### G_offspring

Primary G_offspring endpoint = population-level **expected heterozygosity H_E of the embryo cohort**.

This matches the G_adult metric on the same four-population exposure frame.

Orientation multiplier = `+1`.

Seedlings are not substituted for embryos because seedlings are absent from the two cotton populations and would destroy the common four-population frame.

### C — movement/connectivity

Primary C endpoint = source NMπ **pollen immigration rate m_p** for each population.

Rationale fixed independently of the observed values:

- it is a direct source-estimated movement/connectivity quantity;
- it is available on all four populations;
- the source reports population-specific uncertainty;
- it is more directly interpretable as external pollen connectivity than selfing, DBH effect, or a fitted kernel-shape parameter.

Orientation multiplier = `+1`: larger pollen immigration means greater connectivity support.

Effective number of pollen donors, correlated paternity, pollen-dispersal distance and assignment rate remain secondary/sensitivity quantities only. Do not switch to them after seeing the primary C contrast.

## Effect calculation

For each primary endpoint, use the canonical direct EGWEE Hedges-g estimator:

- `d = (M_frag - M_ref) / s_p`;
- `df = n_frag + n_ref - 2`;
- `J = 1 - 3/(4df - 1)`;
- `g = J d`;
- `V(g) = (n_frag+n_ref)/(n_frag*n_ref) + g^2/[2(n_frag+n_ref)]`.

The dispersion is across the **population-level endpoint values**, not across individual trees, embryos, loci or source model SEs.

Source model SE for pollen immigration is retained as provenance/sensitivity metadata but is not substituted for the fragmentation-unit dispersion in the canonical direct Hedges-g effect.

## Dependence

The three endpoint effects arise from the same four populations and are not independent.

Before Parkia is admitted to a covariance-aware synthesis, reconstruct a working within-cluster covariance from aligned population-level contributions under the existing EGWEE dependence contract. Do not silently set off-diagonal covariance to zero.

If a defensible covariance block cannot be reconstructed, retain the three marginal effects as recovered evidence but do not promote Parkia as a covariance-aware multilayer cluster.

## Source opening and no-rescue rules

Use the source paper tables on the fixed four-population frame.

Do not:

- count adults, embryos, loci or maternal families as fragmentation replicates;
- replace H_E with allelic richness, H_O, F or another genetic metric after observing direction;
- replace large-tree G_adult with small-tree values after observing direction;
- replace embryo G_offspring with the incomplete seedling cohort;
- replace pollen immigration with another pollen metric after observing direction;
- redefine the fragmentation exposure from source outcomes;
- code absent seedlings or missing quantities as zero;
- admit a layer unless the exact population values are source recoverable.

Possible terminal states include:

- `SF05_93_recovered_marginal_C_Gadult_Goffspring`;
- `SF05_93_admitted_covariance_aware_C_Gadult_Goffspring`;
- `SF05_93_covariance_not_reconstructable`;
- `SF05_93_source_values_not_reconstructable`.

All terminal outcomes are acceptable.
