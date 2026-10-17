# CFTQ0135 / Comarum multilevel-spatial I-F recovery contract — 2026-09-24

## Programme

Programme identity: `P2_CF01_COMARUM_2014`.

Primary source: Somme, Mayer & Jacquemart (2014), *PLoS ONE* 9:e99295,
doi:10.1371/journal.pone.0099295.

The source followed **14 Belgian populations of Comarum palustre** for three years and quantified
pollinator activity, pollen limitation and seed set together with population- and landscape-scale
spatial structure.

This is a retrospective external recovery. Published directional statements are visible. All
choices below are therefore fixed before EGWEE calculates a response effect.

## Independent unit

Independent fragmentation unit = **population/site**.

The maximum programme n is 14 populations. The 15 within-population insect-observation plots,
individual plants, flowers, visits, pollination treatments, fruits and seeds are nested below
population and never increase n.

Repeated years are repeated measurements of the same populations, not independent landscapes.

## Locked exposure

Primary exposure = the source-defined **population isolation / landscape woody-area cover within
500 m of the population centre**.

The source explicitly defines its landscape-scale isolation variable from woody-area cover in the
500-m buffer. Retain that numeric variable and source coding rather than substituting a different
landscape metric.

Primary EGWEE severity orientation follows the source's isolation semantics: larger source isolation
= stronger landscape isolation. If the archived field is coded as the complementary connected/open
fraction rather than isolation itself, the sign correction must be determined from the source
definition alone before any I or F response values are read.

Population surface and woody-edge closure are secondary spatial components. Within-population floral
density is a lower-scale biological covariate. None replaces the primary 500-m exposure because its
association is stronger.

## Locked I endpoint

Primary I = **total direct pollinator visitation rate to C. palustre**, aggregated to population on
the source observation-effort basis.

If the source only exposes taxon-specific rates, sum the source-defined visitor groups before
population aggregation when this is mechanically possible. Bumble-bee or solitary-bee abundance
alone cannot replace total visitation after their reported relationships are inspected.

## Locked F endpoint

Primary F = **open-pollinated viable seed set**, aggregated to population on the same population/year
frame as I.

Supplemental hand-cross seed set is used only to characterize pollen limitation and is not the
primary F response. The fragmentation effect is evaluated on realized open-pollinated function.

## Year and common-frame rule

Construct one population-level value for each layer using the broadest source-consistent
multi-year aggregation available for the populations with the locked exposure.

Preferred rule, if the same populations are observed across multiple years:

1. retain source year-specific values;
2. average each endpoint within population across available source years after the source's stated
   exclusions;
3. use one I and one F value per population;
4. use the intersection of populations with exposure + I + F.

Do not treat population-year rows as independent fragmentation units.

If missingness prevents a common multi-year population summary, stop rather than choose the year
with the strongest result.

## Gradient effect representation

This programme belongs only to the Fisher-z gradient/generalisation stream.

For I and F separately:

1. calculate Pearson `r` between the frozen landscape-isolation severity and population-level response;
2. calculate `z = atanh(r)`;
3. use variance `1/(n_population - 3)`;
4. orient negative z as lower biological interaction/function with stronger isolation.

Do not dichotomize the 14 populations into low/high isolation and do not convert to Hedges g.

## I-F dependence

On the exact common population frame:

1. regress I and F separately on the frozen isolation axis;
2. retain population-level residuals;
3. calculate `rho_IF`;
4. set `Cov(z_I,z_F) = rho_IF * sqrt(V_I * V_F)`;
5. require a positive-definite 2x2 working covariance matrix.

The covariance is a reconstructed working proxy rather than an exact analytic sampling covariance.

## Admission

Admit one gradient/generalisation programme only if:

- the source 500-m landscape variable is recoverable with unambiguous orientation;
- site/population IDs are recoverable;
- total visitation can be reconstructed at population level;
- open-pollinated viable seed set can be reconstructed at population level;
- at least four populations share exposure, I and F;
- repeated plots/years/flowers are not promoted to fragmentation n.

Admission depends on effect-unit validity, not significance.

## No-rescue rules

Do not:

- replace the 500-m source isolation variable with population area, closure or floral density after seeing results;
- use bumble-bee or solitary-bee response selectively because it is stronger;
- use 15 observation plots/population as independent n;
- use population-year rows as independent programmes;
- select a single year because the pair is clearer;
- replace open-pollinated seed set with hand-cross seed set;
- dichotomize the gradient;
- interpret this natural system as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `comarum_gradient_IF_covariance_aware`;
- `comarum_isolation_orientation_not_recoverable`;
- `comarum_population_I_not_recoverable`;
- `comarum_population_F_not_recoverable`;
- `comarum_common_population_frame_insufficient`;
- `comarum_covariance_not_positive_definite`.

All outcomes are retained.
