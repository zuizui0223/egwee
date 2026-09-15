# ML016 Atamisquea source-frame preflight

## Passed structural checks

- Four replicated landscape sites: 1, 2, 3, 5.
- Each site contains continuous forest and a source-defined small fragment (<1 ha); large fragment is also available but is sensitivity only.
- Appendix I reports site-by-habitat among-plant means for both targeted endpoints.
- The source states that, except where explicitly noted, pollen-tube, fruit-set and seed-set data came from the same sampled individuals.
- PT and FS are complete for the same four sites in continuous forest and small fragments.

## Primary effect unit

The independent fragmentation replicate is site. The materialized source table therefore carries four site means per arm for each layer. Plant counts and within-site SDs are retained only as provenance/precision metadata and are not used as `n` for the primary Hedges-g contrast.

## Primary vectors

I / PT:

- continuous: site 1 = 11.8; site 2 = 10.4; site 3 = 10.8; site 5 = 16.7
- small fragment: site 1 = 10.5; site 2 = 7.0; site 3 = 8.2; site 5 = 14.1

F / fruit set:

- continuous: site 1 = 0.50; site 2 = 0.30; site 3 = 0.46; site 5 = 0.36
- small fragment: site 1 = 0.34; site 2 = 0.26; site 3 = 0.39; site 5 = 0.27

## Remaining checks before admission

1. reproduce Hedges-g and sampling variance under the repository's canonical `SMD`/`vtype=LS` implementation using n=4 site means per arm;
2. construct an auditable paired-site cross-layer dependence proxy without using within-site plants as habitat replicates;
3. run the unchanged cluster-level state-separation diagnostic;
4. only then add ML016 and rerun the omit-ML001 Fisher sensitivity.
