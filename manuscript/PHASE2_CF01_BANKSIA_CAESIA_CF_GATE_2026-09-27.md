# CFTQ0313 Banksia sphaerocarpa var. caesia linked C-F gate — 2026-09-27

## Programme

Programme identity: `P2_CF01_BANKSIA_CAesia_2012_2013`.

Linked sources:

- Llorens et al. (2012), *Molecular Ecology* 21:314–328,
  doi:10.1111/j.1365-294X.2011.05396.x;
- Llorens et al. (2013), *Biological Conservation* 164:129–139,
  doi:10.1016/j.biocon.2013.05.011.

These papers form one biological fragmentation programme, not two independent programmes.

## C layer is publicly recoverable

The 2012 study sampled **one large and eight small remnant populations** and measured mating-system
and pollen-dispersal responses.

Its Dryad dataset (doi:10.5061/dryad.pm251177) publicly exposes:

- adult genotypes and coordinates;
- progeny and maternal genotypes;
- population codes.

The source reports population-level outcrossing, pollen-pool differentiation, neighbourhood size,
pollen-dispersal distance and pollen immigration.

Thus the C/mating-connectivity programme identity and population coding are source-backed.

## F layer in the linked 2013 paper

The 2013 paper tests effects of remnant shape on:

- plant size;
- inflorescence / cone reproductive output;
- seed size;
- germination;
- seedling size and survival.

It also reports that paternal diversity is associated with seed size and progeny performance,
strongly linking the reproductive/fitness study to the mating-system programme.

However, the audited public reporting surface provides the article abstract/highlights rather than
an authoritative population-level reproductive-output table or raw F dataset.

No public 2013 data deposit was identified that supplies remnant IDs with direct reproductive output
and compatible marginal sampling variance.

## Effect-unit decision

Genotypes from the 2012 Dryad deposit cannot be used to manufacture the missing 2013 F marginal.

The biological linkage between paternal diversity and reproductive/progeny outcomes does not by
itself supply a direct C-F meta-analytic effect.

A direct programme would require:

1. the exact 2013 remnant IDs;
2. demonstrated overlap with the 2012 remnant/campaign frame;
3. a frozen direct F endpoint such as cone/seed reproductive output;
4. remnant-level F values or an effect-unit-valid standardized marginal variance;
5. one dependence representation for the linked C/F cluster.

Those requirements are not met by the current public reporting surface.

## Terminal status

`blocked_linked_2013_population_F_marginals_not_publicly_recoverable`

Direct C-F programme increment: **0**.

The programme remains strong mechanism evidence that fragmentation geometry and mating structure can
jointly shape reproductive output and progeny performance.

## Reopening condition

Reopen if an authoritative source supplies 2013 remnant-level reproductive-output data or a
compatible standardized F marginal on the same linked remnant frame.

If C and F marginals become valid but within-programme covariance remains unavailable, preserve one
programme and use the frozen cluster-robust fallback rather than setting covariance to zero.

## No rescue

Do not:

- treat the 2012 and 2013 papers as independent K;
- infer the 2013 F vector from 2012 genotype data;
- substitute seedling performance for direct reproductive output after seeing results;
- use maternal plants or seeds as remnant n;
- choose remnant shape, isolation or population size by significance after extraction;
- use abstract-level direction as a standardized effect;
- interpret biological linkage as covariance;
- use the programme to validate a finite EGWE/NEE operator.
