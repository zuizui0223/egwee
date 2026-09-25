# CFTQ0278 Catasetum viridiflavum 1997 direct I-F recovery gate — 2026-09-25

## Frozen target

Programme: `P2_CF01_CATASETUM_2002`.

The recovery contract fixes one direct 1997 I-F programme:

- fragmented = island forest site;
- reference = mainland large-forest site;
- independent unit = site/population;
- common frame = exactly five island + five mainland sites sampled for pollinator abundance in 1997;
- I = site-level *Eulaema cingulata* abundance (bees trapped/day);
- F = 1997 female reproductive success / fruit set on those same sites.

## Public-source audit

The open Journal of Ecology article confirms that pollinator abundance was sampled in 1997 at
five island and five mainland sites on three non-consecutive days per site.

It publishes forest-type bee-abundance summaries:

- island mean = 13.1, SD = 1.16;
- mainland mean = 15.33, SD = 2.21.

The source also reports a significant site-within-forest component for 1997 fruit set and for
pollinarium removal.

However, the public article does **not** provide:

1. the exact identities of the five island sites selected from the ten-island network for baiting;
2. the ten site-level bee-abundance values;
3. the ten matching site-level 1997 fruit-set values;
4. a site-level I/F covariance representation.

The 1999 UConn dissertation landing page is public, but the available full-text link resolves to a
ProQuest route that is not publicly recoverable in the audited access path.

## Decision

Status:
`blocked_1997_common_site_identity_and_site_level_F_vector_not_recoverable`.

This is an **effect-unit/data-recoverability stop**, not an ecological null.

The published 1997 forest-type comparison is consistent with similar average pollinator abundance
and no forest-type fruit-set difference, but EGWEE does not attach `n=5+5` to lower-level or
forest-type dispersion and does not infer a ten-site paired vector from model degrees of freedom.

Direct I-F programme increment: **0**.

## Reopening condition

Reopen only if an authoritative public or author-provided source supplies:

- the exact 1997 five-island/five-mainland bait-survey site identities;
- site-level bee abundance for those sites;
- site-level 1997 fruit set for the same sites.

If valid marginal site effects become recoverable but paired covariance does not, retain one
programme cluster and use the pre-existing cluster-robust fallback. Do not set covariance to zero.

## No rescue

Do not:

- use forest-type means and SDs with `n=5` unless the dispersion is explicitly site-level;
- infer the five baited islands from the 15-site map;
- infer site values from nested-model degrees of freedom;
- use plant, inflorescence, flower, bee or baiting-day counts as fragmentation n;
- substitute 1996 or 1998 fruit set;
- digitize figures to invent site-level fruit set;
- treat nonsignificance in 1997 as equivalence;
- use this programme to validate an EGWE/NEE finite operator.

All terminal outcomes are retained.
