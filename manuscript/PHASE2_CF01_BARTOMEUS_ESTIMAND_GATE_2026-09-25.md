# CFTQ0202 Bartomeus landscape I-F estimand gate — 2026-09-25

## Candidate

Programme identity: `P2_CF01_BARTOMEUS_2010`.

Primary source: Bartomeus, Vilà & Steffan-Dewenter (2010), *Journal of Ecology* 98:440–450,
doi:10.1111/j.1365-2745.2009.01629.x.

The source uses **14 independent riparian sites** along a landscape-composition gradient. At every
site, invaded and non-invaded transects are paired and the Raphanus sentinel experiment is repeated
before and during *Impatiens glandulifera* flowering.

## Why this is not yet one registered gradient

The paper characterizes landscape composition with:

- agricultural land cover;
- forest cover;
- grassland cover;

across **500–3000 m radii**.

The source prespecifies different radii for different pollinator guilds (3000 m for bumblebees and
honeybees, 500 m for wild bees and hoverflies), fits different before/during models, and reports
minimum adequate models after stepwise selection.

Those choices are scientifically legitimate in the source study, but they mean EGWEE cannot inspect
the published results and then choose whichever combination of:

- land-cover variable;
- radius;
- pollinator guild;
- invasion period;

produces the clearest I-F separation.

## Frozen gate

No numerical EGWEE effect is opened until a source-backed common-site representation is identified
that fixes, independently of response magnitude:

1. one landscape-severity variable;
2. one spatial radius for that variable;
3. one direct Raphanus visitation endpoint;
4. one Raphanus fruit-set endpoint;
5. one common site/period/treatment frame across I and F.

Independent unit = **site**, maximum n = 14. Paired transects, pots, individual plants, flowers and
visits are nested below site.

## Preferred recovery path

Prefer an authoritative raw/source table with site IDs, landscape composition, Raphanus visitation
and fruit set. If raw site-level data are unavailable, do not create a new Fisher-z family by
back-transforming selected mixed-model t statistics from different guild/radius models.

## Terminal outcomes

- `bartomeus_gradient_IF_covariance_aware`;
- `bartomeus_common_landscape_estimand_not_identifiable`;
- `bartomeus_common_Raphanus_IF_site_frame_not_recoverable`;
- `bartomeus_site_level_data_not_recoverable`.

## No rescue

Do not:

- choose agricultural versus forest versus grassland cover by significance;
- choose 500 versus 3000 m by which gives a larger contrast;
- switch pollinator guilds after seeing results;
- select before versus during invasion because one is clearer;
- count invaded/non-invaded transects as independent landscapes;
- use stepwise-selected model t values as if they were one common raw correlation without a
  prospective conversion contract;
- interpret the result as validation of an EGWE/NEE finite operator.

All terminal outcomes are retained.
