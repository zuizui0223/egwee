# CFTQ0124 / Cabralea direct I-F recovery contract — 2026-09-24

## Programme

Programme identity: `P2_CF01_CABRALEA_2015`.

Primary source: Franceschinelli et al. (2015), *Revista de Biología Tropical* 63:515–524,
doi:10.15517/rbt.v63i2.14160.

The source sampled **three fragmented and three continuous Atlantic-forest sites**. Reproductive
output was measured in all six sites, while pollinator visitation was measured in **two fragmented
and two continuous sites**.

This is a retrospective external recovery. Published group-level directions and means are already
visible. The common I-F frame and endpoints below are therefore fixed before any site-level values
are reconstructed.

## Independent unit and common frame

Independent unit = **forest site**.

For the paired I-F analysis, the maximum common frame is:

- fragmented: F1 + F2;
- reference: C1 + C2.

The third fragmented and third continuous sites contribute reproductive-function context only and
do not enter the paired I-F contrast unless direct visitation is independently shown for those same
sites in an authoritative source.

Plants, 30-min observation periods, inflorescences, fruits and seeds are nested below site and never
increase fragmentation n.

## Locked exposure

Primary direct contrast = **fragmented forest versus continuous forest**, exactly as source-defined.

No edge distance, fragment area, plant density or other variable replaces this two-group contrast.

## Locked I endpoint

Primary I = **pollinator visit frequency: number of flower visits per 30 min**, aggregated to one
site-level value for each of F1, F2, C1 and C2.

Use all source-recorded pollinator visits contributing to the published visitation analysis. Do not
select one moth taxon or one observation period because it yields a stronger contrast.

## Locked F endpoint

Primary F = **number of developed fruits per sampled tree**, aggregated to the same four sites.

Fruit number is selected because it is the source's first direct whole-plant reproductive-output
measure and is available from the broader six-site sampling design. On the paired analysis it is
restricted prospectively to F1, F2, C1 and C2 before effect calculation.

Seeds per fruit, fruit weight, seed abortion and seed predation are secondary endpoints and cannot
replace fruit number after seeing results.

## Effect-size representation

If site-level I and F values can be recovered:

1. form two fragmented and two continuous site values for I;
2. form the same two fragmented and two continuous site values for F;
3. calculate canonical EGWEE Hedges `g` for `fragmented - continuous` using **site** as n;
4. orient negative values as lower interaction/reproductive function in fragments.

The very small 2+2 common denominator is retained explicitly. Lower-level plant or observation
counts cannot be used to manufacture precision.

## I-F dependence

If all four sites have paired I/F values:

1. group-center I and F within fragmented and continuous conditions;
2. calculate Pearson `rho_IF` across the four site-level paired observations;
3. set `Cov(g_I,g_F) = rho_IF * sqrt(V_I * V_F)`;
4. require a positive-definite 2x2 working covariance matrix and positive variance of `g_I-g_F`.

With only four paired site observations, this reconstructed covariance is expected to be fragile and
must be labelled as such. If it is undefined or singular, the paired programme does not enter the
covariance-aware direct family.

## Admission

Admit at most one direct I-F programme only if:

- site identities F1/F2/C1/C2 are unambiguous;
- site-level pollinator visitation can be reproduced without using observation periods as n;
- site-level fruit-number means can be reproduced on the same four-site frame;
- both marginal effects and the working covariance are defined under the frozen rules.

Admission is based on effect-unit validity, not significance.

## No-rescue rules

Do not:

- use the 25 trees/site or repeated 30-min observation periods as independent habitat n;
- use the six-site F effect together with the four-site I effect as if they shared one sampling frame;
- replace fruit number with seeds/fruit, fruit weight, abortion or predation because one gives a larger I-F difference;
- select only one fragment/reference site;
- infer site values by decomposing a published GLMM coefficient;
- digitize figures unless a later prospective amendment explicitly authorizes it before values are extracted;
- call a non-significant 2+2 contrast equivalence.

## Terminal outcomes

- `cabralea_direct_IF_covariance_aware`;
- `cabralea_site_level_I_not_recoverable`;
- `cabralea_common_site_F_not_recoverable`;
- `cabralea_four_site_covariance_not_estimable`;
- `cabralea_common_frame_insufficient`.

All outcomes are retained.
