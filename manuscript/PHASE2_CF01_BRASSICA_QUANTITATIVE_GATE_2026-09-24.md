# CFTQ0030 Brassica rapa quantitative gate — 2026-09-24

## Decision

The Guatemala Brassica programme is **design-valid but quantitatively blocked for the direct I-F pair under the current public source route**.

The source defines a strong fragmentation hierarchy:

- 3 Highly Modified (HM) sites with <10% original forest cover;
- 3 Moderately Modified (MM) sites with >15% original forest cover;
- 3–5 experimental B. rapa plots nested within each site;
- plants, flowers, fruits and visits nested below plot/site.

The independent habitat unit is therefore site, with 3 HM versus 3 MM sites.

## Locked endpoints

The recovery contract froze before raw-data inspection:

- I = total legitimate B. rapa floral visitation rate from one-hour plot censuses;
- F = natural/open fruit set;
- primary exposure = HM versus MM;
- fragmentation n = site.

No alternative I endpoint may replace direct visitation after raw-data access.

## Public raw-data audit

Mendeley Data version 1 (doi:10.17632/6jw833yrt4.1) contains one workbook, Data.xlsx.

Its sheets are:

1. PlotInfo — Site, Condition, Plot, Latitude, Longitude;
2. FSetData — Site, Condition, Plot, Plant, FruitSet, Tratam;
3. BeeDivData — bee-diversity sampling in natural vegetation within 100 m around plots.

Thus the public deposit directly exposes the F hierarchy and site/plot identities, but it does **not** expose the one-hour flower-visitation census rows used for the source's direct B. rapa visitation-rate analysis.

The article itself reports that direct visitation was measured once per experimental plot and reports condition-level statistical tests, PCA summaries and Figure 4. Those are insufficient to reconstruct the six-site I vector and between-site dispersion required by the Phase-2 direct Hedges-g contract.

## Fail-closed rule

The following rescue paths are rejected:

- replacing direct B. rapa visitation with surrounding 100-m bee diversity/abundance;
- using plant/plot replication as habitat n;
- reconstructing site values from published test statistics;
- digitizing Figure 4 after source outcomes are visible;
- switching to continuous land-use PC1 because the binary endpoint cannot be recovered.

Therefore:

- new I-F programme increment: **0**;
- direct I-F coverage remains **1/5**;
- F remains recoverable contextual evidence;
- surrounding bee diversity remains an I-like context/sensitivity endpoint, not the frozen primary I endpoint.

Reopen only if the direct plot-visitation census data or equivalent exact site-level summaries become legitimately public.
