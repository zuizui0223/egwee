# CFTQ0030 Brassica rapa Guatemala Phase-2 recovery contract — 2026-09-24

## Audit status

Source: Escobedo-Kenefic et al. (2024), *Do forest reserves help maintain pollinator diversity and pollination services in tropical agricultural highlands? A case study using Brassica rapa as a model*, Frontiers in Bee Science 2:1393431, doi:10.3389/frbee.2024.1393431.

Public data route declared by the source: Mendeley Data dataset `6jw833yrt4/1`.

This is a **retrospective external recovery**. Published methods and result direction were visible during full-text screening before this contract was committed. Therefore no prospective outcome-blind claim is made. The safeguard is deterministic endpoint selection and preservation of the source hierarchy before raw numerical recovery.

## Exposure

Primary direct exposure is the source-defined two-condition forest-remnant contrast:

- **HM — Highly Modified**: sites retaining <10% original forest cover;
- **MM — Moderately Modified**: sites retaining >15% original forest cover.

There are three independent sites per condition.

The source also derives continuous 1-km land-use/forest-cover variables and a land-use PC1. Those remain secondary gradient/generalisation information and do not replace the primary HM–MM contrast after raw data are opened.

Orientation:

- fragmented = HM;
- reference = MM;
- negative oriented effects mean lower interaction/function in HM.

## Independent unit

Primary fragmentation-level independent unit = **site**.

Hierarchy:

`condition > site > experimental plot > plant / flower / inflorescence / visit`.

Each site contains 3–5 experimental plots; each plot initially contains 36 B. rapa plants. Plots, plants, flowers, fruits and visits are nested observations and never increase fragmentation-level n.

Primary direct contrast therefore requires:

- `n_fragmented = 3`;
- `n_reference = 3`.

## Locked I endpoint

Primary I = **total floral visitation rate to B. rapa experimental plots**.

Use the broadest directly observed plot-level visitor-rate measure corresponding to the source's one-hour censuses:

`number of legitimate flower visits per hour`.

If the raw data contain taxon-specific counts, sum across eligible flower visitors before site aggregation. Do not select wild bees, honey bees, syrphids or another taxon because its habitat response is larger.

Native-bee diversity/abundance sampled in the surrounding 100-m radius is retained as sensitivity/context because it is not the same direct plant-visitation endpoint.

## Locked F endpoint

Primary F = **natural/open fruit set of B. rapa** in the experimental plots.

At the lowest recoverable level:

`fruit_set = fruits / flowers`.

Aggregate upward without promoting flowers/plants to independent habitat units:

1. derive plant/inflorescence fruit-set information as supplied by the source;
2. aggregate to plot;
3. aggregate plot values to site with equal site weighting for the fragmentation effect.

Hand-pollination/pollen-limitation and single-visit efficiency experiments are sensitivity/mechanistic evidence and do not replace natural fruit set as the primary F endpoint.

## Primary effect calculation

If site-level I and F vectors can be reconstructed for all six sites:

For each endpoint use the frozen direct Hedges-g rule, HM minus MM:

- `d = (M_HM - M_MM) / s_p`;
- `df = 3 + 3 - 2 = 4`;
- `J = 1 - 3/(4df - 1)`;
- `g = Jd`;
- `V(g) = 1/3 + 1/3 + g^2/[2(6)]`.

The SD used for standardisation must be the between-site SD within HM and MM after valid lower-level aggregation. Plot- or plant-level SD cannot be combined with site n.

## I–F dependence

I and F share the six source sites.

Working dependence is reconstructed by the registered paired-unit proxy:

1. orient site-level I and F to biological support;
2. subtract the HM or MM group mean from each site's endpoint value;
3. calculate Pearson correlation between the two six-site residual vectors;
4. set `Cov(IF) = rho_IF * sqrt(V_I * V_F)`;
5. require the resulting 2x2 covariance matrix to be positive definite.

Then calculate the prespecified pair contrast:

`Delta_IF = g_I - g_F`

with variance `V_I + V_F - 2 Cov(IF)`.

## Admission rule

The programme can enter direct Phase-2 I–F coverage only if the public raw data reproduce:

- six identifiable independent sites;
- 3 HM + 3 MM site labels;
- the locked broad visitation endpoint;
- natural fruit set;
- defensible site-level aggregation for both endpoints;
- Hedges-g marginal effects and a valid dependence block.

If those conditions pass, the programme contributes **one** independent I–F programme, increasing direct I–F coverage from 1/5 to 2/5.

If site IDs or site-level dispersion cannot be reconstructed, the candidate remains blocked; lower-level plot/plant replication is not used to rescue it.

## No-rescue rules

Do not:

- choose bee composition instead of direct visitation because it differs more strongly;
- choose continuous forest PC1 instead of HM–MM because it produces a stronger result;
- count plots as independent fragmentation units;
- count plants/flowers/visits as independent fragmentation units;
- use hand-pollinated fruit set as primary F;
- select pollinator taxa after effect calculation;
- set I–F covariance to zero for convenience;
- infer missing site summaries from published significance tests.

All outcomes are retained.
