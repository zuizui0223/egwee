# CFTQ0165 / Anaxagorea direct I-F recovery contract — 2026-09-24

## Programme

Programme identity: `P2_CF01_ANAXAGOREA_2012`.

Primary source: Braun & Gottsberger (2012), *Nordic Journal of Botany* 30:453–460,
doi:10.1111/j.1756-1051.2012.01256.x.

The source samples **three large Atlantic-rainforest fragments (306–388 ha)** and **three small
fragments (6–14 ha)** and measures beetle pollinator abundance and reproductive output.

This is a **retrospective external recovery**. The published abstract already exposes the
qualitative null result, so endpoint and effect-unit rules are frozen before any fragment-level
numeric extraction.

## Independent unit

Independent unit = **forest fragment**.

Primary direct denominator:

- small fragments: n=3;
- large fragments: n=3.

Marked flowers, beetles, plants, fruits, monocarps and seeds are nested below fragment and never
increase fragmentation n.

## Locked exposure

Primary direct contrast = **small fragment versus large fragment**, exactly as source-defined.

Do not replace this with continuous area, disturbance score, flower abundance or another habitat
quantity after response values are inspected.

## Locked I endpoint

Primary I = **pollinator abundance per flower** using all source-recognized beetle pollinators.

The source reports pollinator abundance for 186 flowers across the six fragments. EGWEE requires
one fragment-level I value per fragment before any direct Hedges-g effect is admissible.

## Locked F endpoint

Primary F = **fruit set = fruits per flower**.

Seed set / monocarps per fruit is retained as a prespecified reproductive sensitivity only and
cannot replace fruit set because one endpoint yields a stronger fragment-size contrast.

## Effect-size representation

If six fragment-level I and F values are recoverable:

1. compute Hedges g for `small - large` separately for I and F;
2. use fragment as n (3 versus 3);
3. orient negative values as lower interaction/reproductive function in small fragments;
4. retain the common six-fragment frame for both layers.

Do not attach flower-level SDs to n=3 fragment groups.

## I-F dependence

On the six paired fragment values:

1. group-center I and F within small and large conditions;
2. calculate residual Pearson rho_IF;
3. set `Cov(g_I,g_F) = rho_IF * sqrt(V_I * V_F)`;
4. require a positive-definite covariance block and positive variance of `g_I-g_F`.

With only six independent fragments this covariance is fragile and must be labelled as a working
proxy.

## Admission

Admit at most one direct I-F programme only if:

- all six source fragment identities are recoverable;
- fragment-level pollinator abundance is recoverable;
- fragment-level fruit set is recoverable;
- the same six fragments support both endpoints;
- lower-level flowers are not promoted to fragmentation n.

Admission depends on effect-unit validity, not significance.

## No-rescue rules

Do not:

- use 186 flowers or 209 marked flowers as independent fragmentation units;
- select seed set instead of fruit set because it yields a preferred result;
- infer fragment means from group-level large/small summaries if individual fragment values are not
  published;
- digitize figures unless a later prospective amendment authorizes it before extraction;
- call a non-significant direct contrast equivalence;
- use the result as validation of an EGWE/NEE finite operator.

## Terminal outcomes

- `anaxagorea_direct_IF_covariance_aware`;
- `anaxagorea_fragment_level_I_not_recoverable`;
- `anaxagorea_fragment_level_F_not_recoverable`;
- `anaxagorea_common_six_fragment_frame_not_recoverable`;
- `anaxagorea_covariance_not_positive_definite`.

All outcomes are retained.
