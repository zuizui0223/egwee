# CFTQ0156 / Schüepp cherry landscape I-F recovery contract — 2026-09-24

## Programme

Programme identity: `P2_CF01_SCHUEPP_CHERRY_2014`.

Primary source: Schüepp, Herzog & Entling, *Proceedings of the Royal Society B* 281:20132667,
doi:10.1098/rspb.2013.2667.

The experiment uses **30 spatially separated landscape sectors** on the Swiss Plateau. Each sector
contains one standardized row of seven planted *Prunus avium* trees.

This is a **retrospective external recovery**. The article's qualitative results are already public,
so the exposure and endpoints below are fixed to prevent post-result choice among the source's
multiple landscape predictors.

## Independent unit

Independent unit = **landscape sector / experimental site**.

Maximum n = 30 sectors.

Trees, flowers, video records, insect visits and fruits are nested below site and never increase
fragmentation n.

The source omits two sites from fruit-set analysis and three sites from visitation analysis because
of low growth/flowering. The paired EGWEE frame is the mechanically determined intersection of
sites with exposure + I + F and is not selected by response direction.

## Locked fragmentation exposure

Primary exposure = **distance to the nearest woody habitat**.

This is the source's explicit habitat-isolation / fragmentation-per-se variable for pollinator
habitat. Higher distance = stronger habitat isolation.

The following source predictors are secondary and cannot replace the primary exposure after results
are visible:

- percentage woody habitat in the 500-m landscape sector (habitat amount);
- distance to the next wild/cultivated cherry tree (conspecific isolation);
- number of cherry trees in the landscape;
- local cherry flower density;
- local heterospecific flower density.

Conspecific cherry isolation is biologically important but represents target-plant spatial
distribution rather than the registered habitat-fragmentation exposure.

## Locked I endpoint

Primary I = **site-level pollinator visitation rate to cherry flowers**, using the source's all
potential-pollinator definition.

Use one response value per experimental site after the source's stated exclusions and aggregation.
Do not select bees, flies, or another visitor subset because it gives a larger relationship.

## Locked F endpoint

Primary F = **site-level open/control fruit set** of the experimental cherry trees.

Use the source open-pollinated control fruit-set quantity. Hand-supplemented fruit set is not the
primary F response.

## Gradient effect representation

This programme belongs only to the Fisher-z gradient/generalisation stream.

On the exact common site frame:

1. compute Pearson r between woody-habitat isolation and I;
2. compute Pearson r between woody-habitat isolation and F;
3. transform each using z = atanh(r);
4. use variance 1/(n_site - 3);
5. orient negative z as lower biological support/function with stronger habitat isolation.

Do not create low/high isolation bins or convert the programme to Hedges g.

## I-F dependence

On the same common sites:

1. regress I and F separately on woody-habitat isolation;
2. retain site-level residuals;
3. calculate residual rho_IF;
4. set Cov(z_I,z_F) = rho_IF * sqrt(V_I * V_F);
5. require a positive-definite 2x2 working covariance matrix.

## Admission

Admit one gradient/generalisation programme only if an authoritative public source exposes:

- exact site IDs;
- woody-habitat isolation;
- site-level pollinator visitation;
- site-level open fruit set;

for a reproducible common frame of at least four sites.

Admission depends on effect-unit validity, not significance.

## No-rescue rules

Do not:

- replace woody-habitat isolation with cherry isolation because the published relationship is stronger;
- replace habitat isolation with woody-habitat amount;
- use seven trees/site or individual flowers/visits/fruits as landscape n;
- choose different site exclusions for I and F after seeing values;
- digitize figures unless prospectively authorized before value extraction;
- use published regression coefficients as if they were site-level Fisher-z correlations;
- interpret this natural experiment as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `schuepp_cherry_gradient_IF_covariance_aware`;
- `schuepp_public_site_values_not_recoverable`;
- `schuepp_common_site_frame_not_recoverable`;
- `schuepp_covariance_not_positive_definite`.

All outcomes are retained.
