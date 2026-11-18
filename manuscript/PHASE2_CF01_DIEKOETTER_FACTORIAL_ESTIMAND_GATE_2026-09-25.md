# CFTQ0229 Diekötter red-clover factorial I-F estimand gate — 2026-09-25

## Candidate

Programme identity: `P2_CF01_DIEKOETTER_2007`.

Primary source: Diekötter et al. (2007), *Oikos* 116:1588–1598,
doi:10.1111/j.0030-1299.2007.15963.x.

The source is a factorial field experiment in red clover. It explicitly manipulates:

- habitat area;
- habitat fragmentation / configuration;
- matrix composition;

and measures both:

- flower-visiting insect abundance / visitation;
- clover seed set / seed production.

This is therefore a genuine experimental I-F candidate.

## Why no effect is opened yet

The published result is intrinsically factorial. The abstract itself emphasizes that pollinator
visitation was especially high in **small clover patches surrounded by bare ground** relative to
larger patches embedded in grass, and structural-equation results propagate changes in visitation
into seed set.

That pattern makes post-result collapse dangerous. EGWEE cannot inspect the factorial outcome and
then define "fragmented" as whichever area × matrix combination maximizes the I-F signal.

## Frozen gate

No numerical EGWEE effect is calculated until authoritative methods/data establish:

1. the exact independent experimental habitat unit;
2. the number of replicates per area × fragmentation × matrix cell;
3. the source coding of habitat area versus fragmentation/configuration;
4. one response-independent fragmentation estimand shared by I and F;
5. one direct visitation endpoint and one direct seed-set/seed-production endpoint on the same
   experimental-unit frame.

Acceptable estimand forms include:

- a source-defined main fragmentation effect with area/matrix retained as prespecified blocking or
  moderator factors;
- a prespecified marginal contrast averaging over matrix/area cells with source-balanced weights;
- a source-defined factorial contrast fixed from design semantics before response values are opened.

## Not permitted

Do not:

- choose "small + bare ground" as the primary fragmentation condition because it has the largest
  published visitation response;
- pool factor cells with unequal or outcome-dependent weights;
- count insects, flowers, inflorescences, seed heads or seeds as independent habitat replicates;
- call matrix composition itself fragmentation if the source treats it as a separate factor;
- split factorial cells into multiple independent programmes;
- use SEM path coefficients from different factor combinations as if they were one common raw
  Hedges-g contrast without a frozen conversion rule.

## Terminal outcomes

- `diekoetter_direct_IF_factorial_covariance_aware`;
- `diekoetter_direct_IF_factorial_cluster_robust`;
- `diekoetter_factorial_fragmentation_estimand_not_identifiable`;
- `diekoetter_experimental_unit_replication_not_recoverable`;
- `diekoetter_common_IF_unit_frame_not_recoverable`.

Until the gate is resolved, direct I-F programme increment = **0**.
