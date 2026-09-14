# ML016 / Swietenia macrophylla 2012 recovery contract

**Locked:** 2026-09-15, before opening the numeric contents of the public supporting-information documents.

## Goal

Test whether Breed et al. (2012), *Ecology Letters* 15:444–452, DOI `10.1111/j.1461-0248.2012.01752.x`, can contribute a fifth independent primary multilayer cluster without ignoring the paper's provenance heterogeneity or manufacturing within-cluster dependence.

The source follows 71 maternal families from 16 Central American populations. Each source mother is classified by local landscape context as either:

- `forest`: conspecifics within 500 m and the tree located in a large remnant forest or forest patch;
- `isolated`: no conspecific observed within 500 m.

Families are sampled across mesic and dry provenances, and the source shows that the strength of mating and fitness responses differs between those provenances.

## Discovery-stage disclosure

This recovery is not outcome-blind. Before this contract was written, the published article tables and qualitative directions were visible: isolated trees show higher correlated paternity and lower progeny growth overall, with stronger disruption in mesic than dry provenances.

The endpoint identities, effect representation, provenance handling and dependence gate below are therefore fixed now and are not optimized after opening the supporting files.

## Independent-unit frame

Candidate primary observational unit = maternal family / source mother tree.

The source sampled mother trees at least 100 m apart along population transects and assigns forest-versus-isolated context to the mother tree itself. Progeny, loci, repeated growth measurements and fruits remain nested below family and cannot increase fragmentation `n`.

This is an individual local-context observational design across 16 populations, not a replicated landscape experiment. Family-level Hedges-g uncertainty therefore inherits the source's observational-unit interpretation and does not prove the absence of all population-level or spatial residual correlation.

If the supporting material shows that the relevant context exposure is only available at a coarser population/landscape level, terminate rather than promote nested families to exposure replicates.

## Locked primary layers

### G_mating

Primary mating-support endpoint = family-level multilocus correlated paternity `r_p`.

Higher `r_p` means siblings are more likely to share a father and therefore implies lower effective pollen-donor diversity. Store raw fragmented-minus-reference Hedges g for `r_p`, then multiply by `-1` so negative oriented effect means reduced mating / pollen-diversity support under isolation.

Do not switch to `t_m`, `t_m-t_s`, heterozygosity or another mating metric after supporting values are opened.

### F

Primary function endpoint = family-level five-year common-garden progeny growth used by the source as its fitness proxy.

Do not switch to another growth time point, germination, survival, heterozygosity or another fitness representation after value access.

## Locked primary contrast

Primary contrast = all source families classified `isolated` versus all source families classified `forest` on the common complete-case family frame.

For each endpoint:

- compute isolated-minus-forest Hedges g;
- use the repository canonical `metafor::escalc(measure="SMD", vtype="LS")` variance convention:

`V(g) = 1/n_isolated + 1/n_forest + g^2 / [2(n_isolated+n_forest)]`.

The source Table 1 reports 24 isolated and 47 forest families overall. The public common frame, if recovered, is authoritative; missing rows are not back-filled from group summaries.

## Prespecified provenance sensitivity

Mesic and dry provenance are not separate independent studies or clusters.

If family rows expose provenance, calculate the same isolated-versus-forest endpoint contrasts separately within mesic and dry provenance as a heterogeneity sensitivity. These stratum-specific effects do not add to the primary effect count and cannot be selected based on which one is stronger.

The primary all-family effect remains the locked cluster endpoint because landscape context is the source-defined fragmentation exposure. Provenance sensitivities are used to interpret heterogeneity and claim ceiling, not to create extra systems.

## Within-cluster dependence gate

ML016 requires a covariance-aware G_mating/F block for primary admission.

Only if the same public family rows expose both `r_p` and growth:

1. orient family-level mating support as `-r_p`;
2. if provenance is present, center both support and growth within the four source cells `mesic-forest`, `mesic-isolated`, `dry-forest`, `dry-isolated`; otherwise terminate rather than silently ignore the source's demonstrated provenance effect;
3. calculate the Pearson correlation of those paired centered family vectors;
4. set `Cov_GF = rho * sqrt(V_G * V_F)`;
5. require a finite positive-definite 2x2 working covariance matrix.

Do not infer the covariance from Table 2 percent deviance explained, group means/SDs, population-level Appendix S3 correlations, or Figure 3. Do not set covariance to zero and do not add a numerical ridge.

If family-level paired values are not publicly recoverable, the two marginal effects may be retained descriptively if valid, but ML016 terminates as `dependence_not_reconstructable` and adds zero primary effects.

## Source-opening order

1. lock this contract;
2. retrieve the three public supporting-information files (`ele0015-0444-SD1.doc`, `SD2.doc`, `SD3.doc`) through an ordinary public source;
3. inspect file names, headings and table schemas first;
4. determine whether any supplement contains a family-keyed table with context, provenance, `r_p` and growth;
5. only if such a common family representation exists, freeze exact field mapping and open numeric family rows once;
6. calculate primary and provenance-sensitivity effects and paired covariance;
7. retain admission, null, heterogeneous or blocked outcomes without endpoint rescue.

## No-rescue rules

Do not:

- digitize Figure 3 to manufacture family values;
- back-calculate paired covariance from regression R² / percent deviance explained;
- use Appendix S3 population correlations as if they were family-level covariance;
- replace `r_p` with `t_m` because it gives a stronger result;
- erase mesic/dry heterogeneity after seeing it;
- use progeny or loci as independent `n`;
- use group-level SD with family `n` if the source representation does not support that estimand;
- set covariance to zero;
- count mesic and dry strata as separate studies.

## Possible terminal states

- `ML016_admitted_Gmating_F_covariance_aware`;
- `family_level_pair_table_recovered_but_context_or_provenance_missing`;
- `family_level_rp_not_reconstructable`;
- `family_level_growth_not_reconstructable`;
- `common_family_frame_insufficient`;
- `dependence_not_reconstructable`;
- `source_access_blocked`.

All terminal states are retained.
