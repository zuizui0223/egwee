# CFTQ0202 Bartomeus landscape I-F estimand gate — resolved 2026-09-27

## Programme

Programme identity: `P2_CF01_BARTOMEUS_2010`.

Primary source: Bartomeus, Vilà & Steffan-Dewenter (2010), *Journal of Ecology* 98:440–450,
doi:10.1111/j.1365-2745.2009.01629.x.

The source uses **14 independent riparian sites** and places paired invaded/non-invaded transects
plus experimental *Raphanus sativus* pots at each site.

The experiment directly measures floral visitation and fruit/seed response, so the biological I/F
content is eligible in principle.

## Why one fragmentation gradient is not source-unique

Landscape structure is represented by several correlated variables:

- percentage agricultural land;
- forest cover;
- grassland cover;

measured across **500–3000 m radii**.

The source additionally prespecifies different radii for different pollinator guilds:

- about 3000 m for social bees;
- about 500 m for wild bees / hoverflies.

Before- and during-*Impatiens glandulifera* flowering periods are analysed separately, and the
published minimum models are obtained after variable selection.

These are legitimate source analyses. They do not define one unique EGWEE fragmentation severity
that can be selected after reading which guild/period/land-cover variable has the clearest result.

## Raphanus common-frame problem

The public article confirms direct *Raphanus* visitation and fruit set at the 14 sites, but it does
not expose one machine-readable common table containing:

1. one locked response-free landscape variable and radius;
2. one broad population/site-level visitation I endpoint;
3. one fruit-set F endpoint;
4. one common period/treatment frame.

Published results are organized by pollinator guild, invasion period and mixed-model term.

Back-transforming whichever selected model coefficient is most convenient would create a new effect
representation after outcome inspection.

## Terminal status

`blocked_common_landscape_estimand_and_Raphanus_IF_site_vectors_not_recoverable`

Direct I-F programme increment: **0**.

Bartomeus remains valuable evidence that invasion and landscape structure affect pollinator
communities at different spatial/seasonal scales. It is not converted into a single multilayer
fragmentation effect without a common source table.

## Reopening condition

Reopen only if authoritative raw/source data provide the 14 site IDs with:

- one prospectively frozen landscape variable/radius;
- one direct Raphanus visitation measure;
- Raphanus fruit set;
- a common period/treatment definition.

## No rescue

Do not:

- choose agricultural versus forest versus grassland cover by significance;
- choose 500 versus 3000 m because one gives a larger I-F contrast;
- switch pollinator guilds after seeing results;
- select before versus during invasion because one is clearer;
- count paired transects or pots as independent landscapes;
- convert selected mixed-model t values into a Fisher-z effect without a frozen conversion rule;
- use this study to validate a finite EGWE/NEE operator.
