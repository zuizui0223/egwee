# ML004 / PS015 Conospermum 2020 recovery closure

## Decision

`ML004_admitted_I_F_covariance_aware` is **not reached**.

Terminal status:

`effect_unit_or_variance_not_reconstructable`

This is a public-source representation boundary, not an ecological null.

## What was recovered

Delnevo et al. (2020), *Biological Conservation* 252:108824, studies flower visitation and pollen limitation across eleven remnant populations along fragmentation-related gradients. The publication-level evidence supports:

- `I_interaction`: flower visitation increases with floral display and with population connectivity;
- `T_partner_trait`: small populations have an impoverished pool of weakly effective pollinators and lack native specialist bees;
- `F_reproductive_function`: pollen quantity limitation occurs broadly, while total pollen limitation is greater in small fragments because pollen quality/compatibility is reduced.

These directions remain source-supported biological evidence.

## Supplement audit

The Elsevier supplementary package resolves to one file only:

`1-s2.0-S000632072030882X-mmc1.docx`

The recovered supplement contains no tabular population-level I/F dataset. It contains:

- a pollinator-assemblage narrative;
- Appendix S1 visitor images;
- Appendix S2 aggregate visitor composition/activity figures;
- Appendix S3 PCA biplots for 2017/2018 using floral display and population size.

No population-level visitation vector, pollen-limitation vector, source coefficient/SE table, or covariance representation is supplied.

## Thesis / repository audit

The ECU thesis landing page is public and identifies the 2020 Biological Conservation paper, but the repository download URL resolves to a `cgi/viewcontent` route that returned HTTP 403 in both web and CI retrieval attempts.

The thesis landing page lists two related public datasets:

1. microsatellite-marker data;
2. the 2019 reproductive-success Dryad dataset `10.5061/dryad.4cg374r`.

It does not list a distinct public raw-data deposit for the 2020 pollinator/pollen-quality campaign.

## Why the 2019 dataset is not used as F for ML004

The 2019 Ecology and Evolution study has public plant-level fruit/seed data across twelve populations. It is a different publication/campaign and is retained separately in the Conospermum programme provenance.

The ML004 contract was locked before source opening and forbids row-joining that 2019 reproductive dataset to 2020 visitation simply because populations/species overlap. No source recovered here establishes that the 2019 plant observations are the synchronized F observations underlying the 2020 eleven-population pollen-quality experiment.

Therefore the 2019 data cannot rescue ML004.

## Why ranges / figures are insufficient

The reported visitation ranges (`1.5%` to `74.3%` across floral display; `1.3%` to `5.6%` across connectivity) identify direction but do not provide a population-level effect and sampling variance.

Likewise, verbal evidence of greater pollen-quality limitation in small fragments does not provide the paired eleven-population F effect needed for the same-exposure covariance-aware cluster.

The preregistered contract forbids:

- inferring Fisher z from ranges;
- converting p-values or verbal significance into effects;
- digitizing a favourable fitted line after seeing its direction;
- silently setting I-F covariance to zero;
- using nested flowers/visits/treatments as fragmentation-population `n`;
- importing the 2019 F data as synchronized 2020 observations.

## Resulting EGWEE state

ML004 remains a **source-supported multilayer candidate but not an admissible quantitative cluster**.

The admissible set remains:

1. ML001 Serapias — C/F/G_adult;
2. ML002 Brosimum — C/F;
3. ML003 Spondias — C/G_adult.

General denominator: **3 independent clusters / 7 primary effects**.

Covariance-aware C-F denominator: **k=2**.

## Reopening rule

Reopen ML004 only if a source/author archive supplies either:

- population-level 2020 visitation and pollen-limitation values on the same eleven-population frame with a common fragmentation exposure; or
- source model coefficients plus compatible uncertainty/covariance for both layers under the same exposure.
