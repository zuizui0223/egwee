# CFTQ0121 / Plectritis connectivity I-F recovery contract — 2026-09-24

## Programme

Programme identity: `P2_CF01_PLECTRITIS_ISLAND_CONNECTIVITY_2015`.

Primary source: Adderley & Vamosi (2015), *International Journal of Plant Sciences* 176:186–196,
doi:10.1086/679617.

The source maps/caption **12 Plectritis congesta sampling localities** across Vancouver Island and
smaller Gulf Islands in endangered Garry-oak / maritime-meadow habitat. However, the published
model table labels the visitation analysis **N = 13 sites**. That internal denominator discrepancy
must be reconciled before any EGWEE numerical recovery.

This is a retrospective external recovery. Published qualitative results are already visible, so
the exposure, I endpoint and F endpoint are frozen here before EGWEE calculates any effect.

## Independent unit and denominator reconciliation gate

Independent unit = **Plectritis population/site**.

The quantitative gate is closed until an authoritative source identifies the exact site set used
jointly for connectivity, visitation and seed production. EGWEE does not choose 12 or 13 by
convenience or by which denominator yields a preferred result.

Flowers, plants, individual visitors, visitor taxa, observation bouts and seeds are nested below
site and never increase n.

## Locked exposure

Primary exposure = the source-defined **habitat connectivity within a 1-km radius** around each
Plectritis patch/site.

The source connectivity metric is retained exactly once its numeric definition is recovered from
the article/supplement. Because higher connectivity means less isolation, orient the registered
gradient as:

`fragmentation_severity = - source_connectivity`.

Do not replace connectivity with island size, Vancouver-versus-Gulf-island identity, floral display,
Plectritis density or co-flowering diversity after seeing response values.

## Locked I endpoint

Primary I = **total floral visitation rate to Plectritis congesta** at site level.

The source counted pollinator-functional-group visits during standardized observation effort.
Reconstruct the broadest total visitation quantity available on all sites and standardize by the
source observation effort if required.

Visitor species richness, phylogenetic diversity, functional-group composition, solitary-bee
fraction and potential geitonogamy index are secondary/descriptive responses. They cannot replace
total visitation because they show a stronger connectivity association.

## Locked F endpoint

Primary F = **Plectritis seed production / maternal female fitness** at site level, using the
source's direct seed-production quantity.

If several mathematically equivalent seed-production fields exist, use the one used as the source
seed-production response in the published model set. Do not substitute selfing, fruit phenotype or
another downstream trait.

## Common-frame rule

Use only sites with all three of:

1. source connectivity;
2. locked total-visitation I;
3. locked seed-production F.

Missing sites are not imputed. The common site count is determined before correlation effects are
calculated.

## Gradient effect representation

This programme belongs only to the Fisher-z gradient/generalisation stream.

For I and F separately:

1. calculate Pearson `r` between `fragmentation_severity` and the site-level endpoint;
2. calculate `z = atanh(r)`;
3. use variance `1/(n_site - 3)`;
4. negative z means lower interaction or reproductive function with greater isolation.

Do not dichotomize islands/sites or convert this programme to primary Hedges g.

## I-F dependence

On the common site frame:

1. regress I and F separately on the locked fragmentation-severity axis;
2. retain site-level residuals;
3. calculate their Pearson correlation `rho_IF`;
4. set `Cov(z_I,z_F) = rho_IF * sqrt(V_I * V_F)`;
5. require the 2x2 working covariance matrix to be positive definite.

This is a reconstructed working dependence proxy, not an exact analytic covariance.

## Admission

Admit one gradient/generalisation programme only if:

- the 12-locality map versus N=13 visitation-model denominator is reconciled from an authoritative source;
- the exact source connectivity definition and common site identities are recoverable;
- a direct site-level total-visitation quantity is reproducible;
- the direct site-level seed-production response is reproducible;
- at least four common sites remain;
- no visitor, plant or seed observations are promoted to independent fragmentation units.

Admission depends on effect-unit validity, not significance.

## No-rescue rules

Do not:

- choose 12 or 13 sites because one denominator produces a preferred effect;
- substitute island identity or island area for the frozen 1-km connectivity metric;
- select visitor phylogenetic diversity or solitary-bee visitation because it predicts seed production;
- use visitor taxa or observation bouts as independent n;
- select only Gulf Islands or only Vancouver Island sites;
- dichotomize connectivity;
- convert the programme to binary Hedges g;
- treat this natural-island system as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `plectritis_gradient_IF_covariance_aware`;
- `plectritis_site_denominator_not_reconciled`;
- `plectritis_connectivity_definition_not_recoverable`;
- `plectritis_site_level_I_not_recoverable`;
- `plectritis_site_level_F_not_recoverable`;
- `plectritis_common_site_frame_insufficient`;
- `plectritis_covariance_not_positive_definite`.

All outcomes are retained.
