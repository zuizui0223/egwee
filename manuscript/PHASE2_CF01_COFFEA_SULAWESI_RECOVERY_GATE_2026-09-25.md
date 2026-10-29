# CFTQ0272 Coffea canephora Sulawesi recovery gate — 2026-09-25

## Frozen target

Programme: `P2_CF01_COFFEA_SULAWESI_2003`.

Primary article: Klein, Steffan-Dewenter & Tscharntke (2003), *Journal of Applied Ecology*
40:837–845, doi:10.1046/j.1365-2664.2003.00847.x.

Linked umbrella dissertation: Klein (2003), *Bienen, Wespen und ihre Gegenspieler in
Kaffee-Anbausystemen auf Sulawesi: Bestäubungserfolg, Interaktionen, Habitatbewertung*,
doi:10.53846/goediss-1814.

The frozen retrospective contract requires one common 15-site frame containing:

- forest distance;
- broad total coffee flower-visiting bee abundance / visitation (I);
- open-pollinated fruit set (F).

Independent unit = agroforestry system/site.

## What the article exposes

The source uses 15 agroforestry systems and measures:

- distance to old-growth rainforest;
- light intensity;
- coffee and non-coffee blossom cover;
- flowering-plant richness;
- social and solitary bee species/individuals;
- open and hand-crossed fruit set.

Forest distance ranges from the forest margin to about 900 m.

The article provides a direct forest-distance relationship for open fruit set and guild-specific
forest-distance results for social bees.

## Frozen-I mismatch

The pre-audit contract deliberately selected the **broad all-bee abundance/visitation** endpoint to
avoid choosing a guild from published response strength.

In the article's reported source models:

- all-bee species richness has a marginal forest-distance term;
- all-bee individuals are represented by light/blossom terms in the retained model;
- social-bee species and social-bee individuals have explicit forest-distance terms;
- open fruit set has an explicit forest-distance term.

The paper does not print one 15-site vector for the frozen broad all-bee I endpoint.

Therefore EGWEE does not replace the frozen I with social-bee richness, social-bee abundance or a
guild-specific response after seeing that those source relationships are stronger or more
convenient.

## Dissertation access audit

The linked dissertation is the authoritative umbrella source for the same Sulawesi coffee work and
may contain the needed site tables. Its legacy public full-text URL is identifiable, but the current
automated retrieval route does not reproducibly return the PDF bytes.

The dissertation cannot be counted as a second programme and inaccessible rows are not reconstructed
from figures or selected regression coefficients.

## Decision

Status:
`blocked_primary_total_bee_site_vector_not_publicly_recoverable`.

No Fisher-z I-F pair is admitted.

This is a **recoverability/endpoint-lock STOP**, not a claim that landscape isolation has no effect
on coffee pollination.

## Reopening condition

Reopen only if an authoritative source supplies all common-site values for:

1. forest distance;
2. total bee abundance/visitation under the source observation effort;
3. open-pollinated fruit set.

If those 15-site vectors become available, use the already-frozen distance exposure and dependence
rule. Guild-specific responses remain sensitivities.

## No rescue

Do not:

- switch the primary I endpoint to social-bee richness or abundance;
- switch from total abundance to bee species richness;
- select a local shade/blossom variable instead of forest distance;
- digitize scatterplots to manufacture a 15-site vector;
- back-transform selected stepwise-model t statistics into a new raw-data effect;
- count the linked dissertation as a second programme;
- interpret the empirical result as validation of an EGWE/NEE finite operator.

All terminal outcomes are retained.
