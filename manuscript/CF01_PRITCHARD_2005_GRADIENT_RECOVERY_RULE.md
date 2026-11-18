# CFTQ0350 / Pritchard custard-apple gradient recovery rule — 2026-09-25

## Status

Programme identity: `P2_CF01_PRITCHARD_2005`.

Primary source: Pritchard (2005), James Cook University M.Sc. thesis,
*The unseen costs of agricultural expansion across a rainforest landscape: depauperate pollinator
communities and reduced yield in isolated crops*.

This is a **retrospective external recovery**. The source regression, orchard identities and
open-pollination orchard means were visible before this rule was written. The rule exists to prevent
post hoc endpoint, transformation and site-frame selection.

## Landscape exposure

The source selected custard-apple orchards by distance to naturally occurring rainforest and uses
the term crop isolation for this landscape position.

Primary exposure:

`log_distance_to_rainforest_km = ln(distance_to_nearest_rainforest_km)`.

Higher exposure = greater orchard isolation from rainforest.

The source explicitly cautions that distance is not experimentally replicated and can be confounded
with other landscape gradients such as rainfall and north-south position. EGWEE therefore treats
this as **observational landscape-position generalisation evidence**, not a causal isolation effect.

## Independent unit

Independent unit = **orchard/site**.

Flowers, trees, arthropod individuals, pollination treatments and fruits are nested below orchard.

## Primary I effect

Primary I = **total abundance of all floral visitors to 200 female custard-apple flowers per
orchard**.

The source Chapter 3 samples nine orchards and fits:

`ln(total floral visitor abundance) ~ ln(distance to rainforest)`.

It reports:

- n = 9 orchards;
- R² = 0.573;
- negative slope;
- F(1,7) = 9.39;
- p = 0.018.

The primary I correlation is therefore recovered deterministically as:

`r_I = -sqrt(0.573)`.

Then:

- `z_I = atanh(r_I)`;
- `V_I = 1/(9-3)`.

Do not substitute visitor richness, non-cosmopolitan abundance, or one pollinator guild after
seeing their published results.

## Primary F effect

Primary F = **open-pollinated fruit initiation proportion**.

Chapter 4 gives source orchard means for the five orchards in the pollination experiment:

| orchard | distance km | open fruit initiation |
|---|---:|---:|
| Briggs Lease | 0.1 | 0.11 |
| Cummings | 0.5 | 0.04 |
| Kilpatrick | 5.5 | 0.02 |
| Lavers | 9 | 0.02 |
| Samanes | 12 | 0.03 |

These five orchards are an explicit subset of the nine I orchards.

The source states that natural logarithms of distance and fruit initiation were used for the
distance analysis. EGWEE therefore fixes:

`r_F = cor(ln(distance_km), ln(open_fruit_initiation))`.

Then:

- `z_F = atanh(r_F)`;
- `V_F = 1/(5-3)`.

A raw-proportion correlation may be retained as a transformation sensitivity but cannot replace the
log-log primary result.

## Dependence / frame overlap

The F frame is an exact five-orchard subset of the nine-orchard I frame.

The public source does not expose the nine numeric I orchard values in a table and therefore does not
permit the five-overlap I/F residual covariance to be reconstructed without figure digitization.

Under the frozen 2026-09-12 multilayer-cluster amendment:

- both marginal Fisher-z effects are retained in **one programme cluster**;
- covariance is **not set to zero**;
- the programme uses the declared **cluster-robust fallback** at the cross-programme stage;
- no covariance-aware within-programme I−F p-value is calculated.

## Admission

Admit one retrospective gradient/generalisation programme if:

1. the source nine-orchard I regression statistics reproduce exactly;
2. the five F orchard means reproduce exactly;
3. the five F orchards are verified as a subset of the nine I orchards;
4. both Fisher-z marginal variances are finite;
5. no lower-level flowers, trees or fruits are used as orchard n.

This programme contributes **zero** primary direct Hedges-g programmes.

## No rescue

Do not:

- digitize Figure 3.2 to manufacture the nine I orchard values;
- predict five I values from the fitted regression line and treat predictions as observations;
- use the Chapter 4 tree-level F(1,48) regression as orchard-level n;
- select visitor richness or exotic-excluded abundance because it changes the result;
- switch F to hand-pollinated fruit initiation;
- treat the five-orchard and nine-orchard frames as independent programmes;
- set unknown covariance to zero;
- claim causal rainforest-distance effects;
- interpret this programme as validation of an EGWE/NEE finite operator.

All outcomes are retained.
