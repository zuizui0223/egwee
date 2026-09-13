# C07 / candidate ML010 — *Penstemon hirsutus* 2019 isolation-cluster recovery contract

**Locked:** 2026-09-13, before quantitative values from the public microsatellite files are opened.

## Goal

Test whether the 2014 Chicago experimental green-roof network can contribute a fourth independent multilayer fragmentation/isolation cluster using a common population-level exposure and the same ten experimental roof populations.

This gate is separate from the paper's three natural-prairie versus three established-green-roof adult-genetic comparison. The 3+3 establishment comparison is not merged into the ten-roof experimental C/G_offspring cluster.

## Independent-unit frame

Primary independent unit = experimental roof population.

- ten experimental roof populations are the landscape units;
- five potted parent plants per roof are nested below roof;
- offspring and microsatellite loci are nested observations used to estimate roof-level responses;
- parent plants, offspring and loci never become isolation/fragmentation replicates.

## Locked exposure

Primary exposure = the source-defined **mean distance from each experimental roof population to the other nine experimental roofs**.

Define isolation severity as:

`isolation_severity = z(mean_distance_to_other_roofs)`

Higher values therefore mean greater isolation within the experimental roof network.

Do not switch after outcome access to roof area, height, local floral richness, nearest-neighbour distance, geographic pair distance, or any predictor selected because it strengthens C or G.

## Locked primary layers

### C — movement/connectivity support

Primary C endpoint = **between-roof pollen support fraction per maternal roof population**, using the source study's parentage assignments.

Preferred population statistic:

`between_roof_fraction = n_offspring_assigned_to_father_on_other_roof / n_offspring_with_source-classifiable_paternity`

The exact denominator must follow the source parentage classification rules and be fixed from the available assignment output/schema before values are summarized.

The source used CERVUS maximum-likelihood parentage, including source-specific confidence/tie handling. Do **not** casually reproduce or replace that procedure from microsatellite genotypes. C is recoverable only if one of the following is available through an ordinary source route:

1. source parentage/assignment output at offspring level;
2. a source table with roof-level counts sufficient to reconstruct the same between-roof fraction;
3. code/output supplied by the source that reproduces the reported classifications.

If only raw genotypes are available, terminate C as `source_parentage_assignments_not_reconstructable` rather than substituting a new parentage algorithm.

### G_offspring — genetic state

Primary G_offspring endpoint = roof-level offspring expected heterozygosity `H_E`, reconstructed from the experimental offspring microsatellite file if population labels and diploid genotypes are directly available.

Uncertainty must be population-level and must preserve loci/offspring as nested observations. The exact bootstrap/uncertainty rule will be locked in a second amendment **before genotype values are summarized**, after the raw schema and number of loci/populations are confirmed.

Do not switch to allelic richness or F_IS because its observed direction is more convenient. Those may be prespecified sensitivities only after the primary H_E rule is fixed.

## F layer

Reproductive-function measurements in the publication are not admitted in this first gate. F may be added only if an ordinary source file exposes exact roof-level reproductive summaries under the same ten-roof exposure. Do not digitize figures or back-calculate roof values from relationship tests.

## Dependence and effect representation

If both C and G_offspring are reconstructable on the same ten roofs:

1. compute separate population-level associations with the locked isolation severity;
2. orient both so negative values mean reduced connectivity/genetic support with increasing isolation;
3. lock the correlation/effect and uncertainty transformation before outcome values are calculated;
4. preserve within-cluster C/G dependence from the paired roof-level contributions or a prespecified roof-level bootstrap;
5. never set C/G covariance silently to zero.

Five parents per roof, offspring counts and loci do not increase the cross-system denominator. If admitted, the entire experimental roof network counts as **one** independent cluster.

## Source-opening order

1. public repository metadata and filenames;
2. CSV headers/schema, row counts and structural role labels only;
3. determine whether source parentage assignments are present;
4. lock exact C denominator and G uncertainty/effect formulas;
5. only then open quantitative genotype/assignment values and calculate effects.

## Schema gate

Expected public files from the paper's data record:

- `NatVsRoof_Microsats_FinalData.csv`;
- `Parentage_Microsats_FinalData.csv`.

The first schema audit may inspect headers, row counts, file sizes and categorical structural labels needed to determine whether rows represent parents/offspring/sites and whether assignment-output columns exist. It must not calculate C/G effects.

## No-rescue rules

Do not:

- merge the 3 natural + 3 established-roof adult-genetics design into the 10 experimental-roof C/G cluster;
- treat five parent plants per roof as five isolation replicates;
- treat offspring or loci as independent roofs;
- replace source parentage with an ad hoc CERVUS-like or distance-based assignment;
- infer between-roof paternity from geographic proximity alone;
- switch the common exposure after observing outcomes;
- manufacture F from figures or nonsignificance;
- count multiple endpoint rows as multiple independent systems.

Possible terminal states include:

- `ML010_admitted_C_Goffspring_covariance_aware`;
- `source_parentage_assignments_not_reconstructable`;
- `offspring_genetic_state_not_reconstructable`;
- `common_roof_overlap_insufficient`;
- `dependence_not_reconstructable`;
- `source_access_blocked`.

All terminal outcomes are acceptable.