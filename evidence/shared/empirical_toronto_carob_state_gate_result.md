# Toronto and Mallorca carob empirical state-gate result

## Locked Toronto urban residual-context replication

The Toronto analysis was prospectively frozen before project-level access to the reproductive outcome values. Whole gardens were held out. The restricted model contained phytometer species, effort-standardised direct visitation, focal floral units and the source-matched garden floral-richness coordinate; the augmented model added urban cover and green-space edge density.

After the response-firewalled case-only normalization of the four already-preregistered phytometer codes, 28 eligible rows from 10 gardens and three phytometer species remained. Adding urban context changed total held-out negative log likelihood by

`Delta NLL = NLL(M1) - NLL(M0) = +4932.9195`,

with a 10,000-draw garden bootstrap 95% interval `[+603.9654, +10953.6611]`.

Decision: **`no_detected_residual_urban_context_information`**.

This means only that, under the locked model and whole-garden transfer criterion, the added urban-context coordinates did not improve prediction after the measured partial pollination/floral state. It does not establish that urbanisation is biologically irrelevant, that the partial state is complete, or that another independently defined process state could not retain residual urban information.

## Locked Mallorca carob N3 process-adequacy test

The N3 carob test was opened only after its endpoint, holdout unit, likelihood, two pollinator-abundance representations, B1/B2 gate sequence, bootstrap rule and no-rescue stop rules were merged to `main`. The primary response was fruit production (`TotalFruits`) with `log(TotalFlowers)` exposure, evaluated by leave-one-orchard-out NB2 predictive likelihood across 20 orchards and 37 orchard-year rows.

Stage A had shown that the deposited workbook retained two non-identical source representations of pollinator abundance, so both were mandatory rather than selecting one after outcomes:

- embedded `FruitProduction.PolinAbun`: `Delta NLL = -0.10195`, orchard-bootstrap 95% CI `[-3.12202, +3.61919]`;
- orchard-year joined `PollinatorAbundance.PolinAbun`: `Delta NLL = -0.09919`, 95% CI `[-3.14415, +3.66453]`.

Both were classified **`no_detected_process_information`**. Therefore the preregistered B1 gate failed and B2 was not opened.

Final decision: **`process_measurement_not_supported_for_primary_endpoint`**.

This is a measurement-adequacy result. It does not show that pollinators do not affect carob reproduction and it does not test whether landscape/management context becomes redundant after an informative process state, because the process coordinate did not first earn held-out predictive adequacy for the locked fruit-production endpoint.

## Joint interpretation

The two systems land on different sides of the empirical gate sequence:

`measurement adequacy -> representation preservation -> residual context`.

Toronto reached the residual-context stage and did not recover transferable urban-context gain after its locked partial state. Carob stopped one gate earlier because direct pollinator abundance did not earn reproducible held-out predictive information for the locked fruit-production endpoint under either source representation.

Together they strengthen the procedural claim, not an urban-island ecological equivalence claim: **upstream context can only be tested for redundancy after the candidate process state itself has demonstrated endpoint-relevant predictive adequacy under an information-preserving representation.**

## Provenance

Toronto: workflow run `32993817229`, artifact `9615678873`, artifact SHA256 `07a0fe1ce25ed625cec03d73d3fa112ac6094328c5926d29d5581837147bef93`.

Carob: one-shot workflow run `33134449528`, artifact `9671498573`, artifact SHA256 `288bd23faada1f5a3e24f3b624c80500afdbda2789cad9cce2a1811b63928346`, frozen contract SHA256 `61be811be8789b86a3cdb019ba8ac1dbf487a6e776775eee982d045cc076084d`.
