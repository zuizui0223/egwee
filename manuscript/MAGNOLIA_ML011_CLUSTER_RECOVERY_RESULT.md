# ML011 / PS002 *Magnolia stellata* recovery result

## Terminal state

`source_population_size_values_not_recoverable`

No C/F effect or covariance was calculated.

## What was locked before numeric supplement opening

The recovery contract fixed:

- independent unit = six seed-sampled populations Y/T/A/B/C/F;
- primary common exposure = the source model's population size, explicitly defined in the paper Methods as **summed basal area (summed size) of adult genets**, not adult-genet count;
- F = population mean seed-production rate;
- C = between-population pollen export only if an auditable population-level export vector/denominator could be reconstructed;
- no substitution of adult-genet count, total siring, study-wide pollen-flow percentage, selfing, gamma, or a different exposure.

The calculation formula was frozen before numeric supplement rows were opened.

## Supplement audit

Publisher electronic supplement:

`12898_2012_239_MOESM1_ESM.docx`

Schema inspection before numeric opening found one table with:

- sink population;
- `Population size`;
- N offspring analysed;
- source-population-of-pollen columns;
- total pollen immigration.

After the calculation lock, numeric rows were opened. The supplement `Population size` values for the six focal populations are:

- Y = 85
- T = 97
- A = 46
- B = 16
- C = 23
- F = 4

These are integer genet-count-scale values and correspond to the study's adult-genet census representation, not the summed-basal-area population-size variable used as the source-defined explanatory variable in the female-reproduction model.

The paper Methods separately defines modelled `population size` as the **summed size of adult genets in the focal population**, with genet size based on basal area of the largest stem. Therefore the supplement's integer population-size column cannot be silently treated as the model exposure fixed by the contract.

## Connectivity structure

The supplement does contain a complete donor-by-sink pollen table on the six focal populations, so a population-level between-population pollen-flow vector is structurally reconstructable. That does not rescue ML011 because the common primary exposure gate fails first.

Per the no-rescue rules, we did not:

- substitute adult-genet count for summed basal area;
- choose a new exposure after seeing pollen-flow values;
- calculate C/F correlations under an unregistered proxy;
- use nested offspring as fragmentation replication.

## Interpretation

Magnolia remains strong mechanistic evidence that fragmentation-related population structure affects female reproduction and between-population mating, but the public representation does not expose the exact six-population values of the source-defined summed-basal-area exposure required for a covariance-aware common-exposure cluster.

Reopen only if the six population-level summed adult-genet basal-area values (or an author-provided equivalent source table) become available. Until then ML011 contributes mechanistic/native-scale evidence, not a fourth admissible EGWEE multilayer cluster.