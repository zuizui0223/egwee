# CFTQ0334 Schlotman spring-ephemeral I-F recovery stop — 2026-09-25

## Programme

`P2_CF01_SCHLOTMAN_2011`.

Source: Holly Lynn Schlotman (2011), *The Effects of Forest Fragmentation on the Reproductive
Success of Spring Ephemeral Wildflowers and Their Pollinators*, Wright State University M.S.
thesis.

The thesis uses 21 forest fragments spanning 3.4–755.6 ha and studies three spring ephemerals plus
Bombus communities.

## What the public thesis recovers

The source provides unusually strong effect-unit provenance.

### Fragment geometry

Table 1 gives fragment area and species/year occupancy for every site.

For *Delphinium tricorne* in 2010, Table 1 identifies 12 reproductive-study fragments.

### Reproductive function

Table 4 publishes 2010 *D. tricorne* site-level averages for:

- flowers per plant;
- fruit development per plant;
- seed production where recovered;
- fruits per flower.

The author later states that average fruit production is the best indicator of *D. tricorne*
reproductive success in this dataset. Thus the primary F candidate is source-supported and
fragment-level.

### Pollinator captures

Bumblebees were surveyed at the union of 2010 *Delphinium* / *Dicentra* sites.
Table 8 and Appendix 1A publish the captured Bombus individuals by site and date.

The source I endpoint, however, is **not raw captured count**. Methods define bumblebee abundance as:

`all bumblebee individuals captured / trapping hours`.

## Effect-unit problem

The methods specify six 10-minute survey points on two different days per site, but then state that
each site had a **minimum** of two total survey hours and that trapping effort was equal for **most**
sites.

Appendix 1A is a capture-event ledger. It does not list zero-catch survey periods or one
authoritative total-trapping-hours value for every site.

This matters empirically: at least Halls Creek has capture records on three dates, demonstrating
that effort was not mechanically two hours at every site.

Therefore the public source permits recovery of:

- fragment area;
- species occupancy;
- fragment-level F;
- bee captures;

but **not the exact source-normalized site-level Bombus abundance vector**.

The common *D. tricorne* 2010 I-F frame also excludes Cemex Linebaugh from the bee table, so the
paired frame would need to be formed explicitly after the source I vector is reconstructed.

## Decision

Status:
`blocked_site_level_Bombus_effort_normalization_not_publicly_recoverable`.

No Fisher-z I-F programme is admitted.

This is a normalization/recoverability limitation, not an ecological null. The thesis reports that
fragment area predicts *D. tricorne* fruit production and that Bombus abundance predicts its
reproductive success, while Bombus abundance itself is not significantly related to fragment area.

## Reopening condition

Reopen only if an authoritative source or field dataset supplies either:

1. total trapping hours for every relevant 2010 site; or
2. the already-normalized site-level Bombus abundance-per-hour vector used by the source.

If recovered, retain fragment area as the response-free exposure and use the same common fragment
frame for I and F. Because source values and directions are now visible, any eventual numerical
recovery is explicitly retrospective.

## No rescue

Do not:

- assume two hours for every site;
- infer zero-catch survey effort from absence in Appendix 1A;
- use raw Bombus capture counts when effort differs;
- switch the primary I endpoint to species richness/diversity merely because Table 8 reports it;
- use plants, flowers, fruits or individual bee captures as fragment n;
- select only *Delphinium tricorne* because its reproductive response is strongest and then count
  other plant species as extra programmes;
- digitize figures to invent normalized abundance.

All outcomes are retained.
