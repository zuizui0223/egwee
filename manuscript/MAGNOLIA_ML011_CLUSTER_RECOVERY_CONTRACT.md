# ML011 / PS002 *Magnolia stellata* cluster-recovery contract

## Goal

Attempt a fourth independent multilayer cluster from Suzuki, Nagamitsu & Tomaru (2013), DOI `10.1186/1472-6785-13-10`, without converting incompatible native-scale model parameters post hoc.

## Independent-unit frame

Primary independent unit = the six seed-sampled populations Y, T, A, B, C and F. Maternal genets, flowers, offspring and mating pairs are nested below population and cannot become fragmentation replicates.

## Locked common exposure

Primary exposure = the source-defined **population size measured as summed basal area (summed size) of adult genets in the focal population**.

This is deliberately NOT the number of adult genets printed in parentheses in Figure 1. The source Methods explicitly defines the modelled population-size variable as summed adult-genet size. Adult-genet count must not be substituted if the summed-basal-area values are unavailable.

Neighbouring population size is retained only as a prespecified secondary exposure if exact population-level values are supplied by the source. No exposure is chosen based on outcome direction.

## F endpoint

Primary `F_reproductive_function` endpoint = source population mean seed-production rate (percentage of ovules developing into filled seeds) for Y/T/A/B/C/F.

The six population means may be used as paired population-level outcome values; maternal-genet observations remain nested.

## C endpoint

Primary `C_movement_connectivity` endpoint = **between-population pollen export from each donor population**, derived only if the electronic supplement exposes donor-to-recipient or otherwise unambiguous between-population siring information on the same six populations.

Preferred representation is a population-level proportion of assigned outcross offspring sired in other populations when the denominator is reconstructable without mixing maternal sampling effort into the donor outcome. If only unnormalised total offspring sired by each population is supplied and no valid between-population export quantity/denominator can be reconstructed, terminate `C_population_vector_not_reconstructable` rather than relabel total male reproductive output as connectivity.

Do not replace C with the paper-wide 6.09% pollen-flow summary, the mating-pair separation coefficient gamma, selfing, or total siring after seeing values.

## Admission rule

Admit ML011 only if:

1. exact six-population source-defined summed-basal-area exposure values are recoverable;
2. F is recoverable for the same six populations;
3. a valid population-level C vector is recoverable for the same six populations under the locked definition;
4. the same exposure can be associated with both C and F without changing scale after outcomes are opened;
5. within-cluster dependence can be reconstructed from paired population contributions/centered values, with a valid covariance representation.

Primary effect representation is a population-level gradient association on the six paired populations. The exact correlation/standardisation formula must be fixed before calculating C/F associations once the supplement schema confirms the required fields. No p-value-only or coefficient-scale conversion is allowed.

## Opening order

1. lock this contract;
2. inspect the electronic supplement schema/labels and confirm whether summed-basal-area population size and between-population siring are represented;
3. only if both are identifiable, freeze the exact calculation formula;
4. open numeric supplement values and calculate the paired C/F cluster once;
5. record positive, null, discordant, or non-identifiable outcomes without rescue.

## No-rescue rules

Do not:

- substitute adult-genet count for summed basal area;
- use maternal genets/offspring/mating pairs as landscape n;
- switch from pollen export to total siring, selfing, gamma, or study-wide pollen-flow percentage after values are seen;
- digitize Figure 1 arrows if the supplement does not provide an auditable population-level C representation;
- select population size versus neighbouring population size by whichever gives a preferred result;
- claim a fourth cluster from native coefficients that lack a common population-level exposure/covariance.

Possible terminal outcomes:

- `ML011_admitted_C_F_covariance_aware`;
- `source_population_size_values_not_recoverable`;
- `C_population_vector_not_reconstructable`;
- `common_population_overlap_insufficient`;
- `covariance_not_reconstructable`;
- `source_access_blocked`.

All terminal outcomes are acceptable.