# CFTQ0215 / Leptonychia 2009 C-F recovery contract — 2026-09-27

## Programme

Programme identity: `P2_CF01_LEPTONYCHIA_2009`.

Primary source: Cordeiro, Ndangalasi, McEntee & Howe (2009), *Ecology* 90:1030–1041,
doi:10.1890/07-1208.1.

Linked historical source: Cordeiro & Howe (2003), *PNAS*,
doi:10.1073/pnas.2331023100.

The 2009 article explicitly extends the same East Usambara fragmentation system to test whether
reduced recruitment can be explained by diminished fecundity, seed quality, predation or abiotic
conditions rather than disperser limitation. It also reports extended observations of disperser
activity.

This is a **retrospective external recovery**. Published qualitative directions are already known.
The rules below therefore prevent selective endpoint/campaign use rather than claiming outcome-blind
confirmation.

## Primary recovery target

Prefer a **single 2009 campaign/common frame** containing both:

- C = direct seed removal / disperser-mediated seed movement;
- F = direct fecundity / realised seed production.

The 2003 source is provenance and linked-process context. It is not concatenated with 2009 simply
because species and landscape are the same.

A cross-paper 2003-C + 2009-F pair is allowed only if an authoritative source table proves the exact
shared fragmentation units and the dependence/campaign relation can be represented explicitly.

## Fragmentation exposure

Primary contrast = source-defined **small forest fragment versus continuous forest**.

The 2003 system identifies four small fragments (2, 9, 13 and 31 ha) outside a large continuous
forest block. The 2009 data must recover its own exact habitat/site identities rather than assuming
the 2003 frame silently persists unchanged.

## Independent-unit firewall

Primary fragmentation unit = **source forest site/fragment or explicitly named continuous-forest
sampling locality**.

Focal trees, watches, fruits, seeds, seed-placement stations, seedlings and transplants are nested
below site and never increase fragmentation n.

If the public data expose only individual-tree rows with a fragment/continuous label but do not
identify independent site/locality membership, EGWEE does **not** treat trees as replicated
fragmentation landscapes. That terminal outcome is retained as an effect-unit STOP.

## Locked C endpoint

Primary C = **direct seed-removal support per source-standardized observation effort** from the
2009 extended disperser-activity sampling.

Use the broad source-defined effective disperser/removal quantity before species-specific selection.
If the source provides a direct fraction/proportion of available seeds removed at the same
site/locality frame, prefer that bounded quantity over an unstandardized raw count.

Bird abundance alone is interaction/process context and does not replace direct seed movement C.

## Locked F endpoint

Primary F = **direct fecundity / realised seed production per reproductive tree or source site**,
aggregated to the same fragmentation unit as C.

Use the source's direct realised crop/seed-production quantity. Seed viability, seed predation,
seedling survival and recruitment are separate endpoints/layers and cannot replace F after outcome
inspection.

## Common-frame rule

A direct C-F programme is admitted only on the exact intersection of independent fragmentation units
with:

1. source habitat/site identity;
2. primary C;
3. primary F.

Missing units are not imputed. Lower-level observations may be aggregated only according to the
source hierarchy fixed before marginal effects are calculated.

## Effect representation

If an eligible source-defined two-group site/locality frame is recovered:

1. calculate canonical EGWEE Hedges `g` for fragment minus continuous forest for C;
2. calculate the same for F;
3. use the frozen LS sampling variance;
4. orient higher C/F as greater biological support/function.

If paired site/locality values are available, reconstruct the working C-F covariance from
group-centered paired units. If dependence is known but covariance cannot be reconstructed while
marginal fragmentation-unit effects are valid, retain one cluster and use the preregistered
cluster-robust fallback at the cross-system stage. Never set covariance to zero by convenience.

## Admission

Admit one direct C-F programme only if:

- at least two independent fragmentation units per condition are defensible;
- C and F share the same exposure and campaign/common frame, or a linked-campaign dependence rule is
  explicitly recoverable;
- marginal variances correspond to the fragmentation-unit level;
- nested trees/seeds/watches do not inflate n.

## No-rescue rules

Do not:

- join 2003 C to 2009 F solely because both papers use *Leptonychia*;
- count focal trees as fragment replicates without site/locality provenance;
- substitute bird abundance for direct seed movement;
- substitute seedling recruitment for F;
- substitute seed quality or predation for F because they are more recoverable;
- select only a year/campaign with stronger fragmentation separation;
- digitize a figure when an authoritative public data file is required by the effect-unit gate;
- interpret a failure of the diminished-fecundity hypothesis as statistical equivalence of C and F;
- use the programme to validate an EGWE/NEE finite operator.

## Terminal outcomes

- `leptonychia_direct_CF_covariance_aware`;
- `leptonychia_direct_CF_cluster_robust`;
- `leptonychia_public_data_no_common_CF_frame`;
- `leptonychia_fragmentation_unit_not_recoverable`;
- `leptonychia_linked_campaign_alignment_not_recoverable`;
- `leptonychia_F_not_direct_fecundity`.

All outcomes are retained.
