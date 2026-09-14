# ML014 / PS020 Eucalyptus socialis 2012 recovery result

## Terminal state

`ML014_admitted_Gmating_F_covariance_aware`

ML014 is admitted as the fourth independent **primary Hedges-g multilayer cluster**.

## Locked frame

The prospective recovery contract was committed before public numeric outcome rows were opened.

- primary exposure: source-defined within-Monarto landscape context;
- fragmented: `MONLOW`, isolated pasture trees;
- reference: `MONHIGH`, small-remnant woodland trees;
- Yookamurra (`YOOKA`) is sensitivity/source context only and is excluded from the primary contrast;
- independent unit: maternal tree / progeny family;
- public family table: 46 rows total (`MONLOW=13`, `MONHIGH=15`, `YOOKA=18`);
- primary complete-case Monarto frame: 28 families (`13` fragmented, `15` reference).

The paper reports 16 mothers in the small-remnant context, but the public family-level table contains 15 `MONHIGH` rows. The missing family is not back-filled; the public common frame is used as observed.

The source explicitly estimates family-level mating parameters and models family-level mating against growth. Monarto low- and medium-density trees are sampled within the same broad landscape, isolated pasture trees occur as separated small clusters/often single trees, small-remnant mothers come from woodland contexts, and near-neighbour maternal sampling was avoided. This is therefore treated as a source-supported maternal-family observational frame rather than a site-level summary expanded by progeny counts.

## Primary effects

### G_mating — family correlated paternity `r_p`

The locked endpoint is family-level multilocus correlated paternity. Higher `r_p` indicates fewer effective pollen donors, so the fragmented-minus-reference Hedges-g effect is multiplied by `-1` to orient the result as biological support.

Source summaries on the admitted family frame:

- fragmented mean `r_p = 0.46923077`, SD `0.36397027`;
- reference mean `r_p = 0.19133333`, SD `0.12408906`;
- raw fragmented-minus-reference Hedges `g = +1.02391388`;
- orientation multiplier `-1`;
- oriented mating-support effect: **`g = -1.02391388`**;
- metafor-LS sampling variance: **`0.16231117`**.

Fragmentation therefore strongly reduces pollen-donor-diversity/mating support in this Monarto contrast.

### F — family mean progeny growth

The locked function endpoint is family-level mean plant height from the common-garden experiment, already present on the same family rows.

- fragmented mean growth `35.75461538 cm`, SD `7.86124949`;
- reference mean growth `37.82733333 cm`, SD `6.98739218`;
- oriented/direct Hedges `g = -0.27180887`;
- metafor-LS sampling variance: **`0.14490903`**.

Growth is lower in isolated-pasture families, but the point estimate is much smaller than the mating-support deterioration.

## Dependence

The two effects use the same 28 maternal families. Using family mating support `-r_p` and growth, group-centered within the two Monarto contexts:

- residual outcome-correlation proxy `rho = +0.32672987`;
- working sampling covariance `Cov(G_mating,F) = +0.05010843`;
- 2x2 determinant `0.02100950`.

The working covariance matrix is positive definite, so the prospectively declared covariance-aware admission gate passes.

## Within-system state separation

For the single G_mating-minus-F contrast:

- difference `-0.75210501` Hedges-g units;
- variance `0.20700334`;
- SE `0.45497620`;
- z `-1.65306450`;
- two-sided / cluster p `0.09831774`.

This system therefore contributes an independent multilayer cluster even though it does not individually reject layer exchangeability at 0.05. Admission never depended on significance.

## Biological interpretation

The geometry is **directionally concordant but unequal in strength**: fragmented isolated-pasture families show a strong reduction in pollen-donor diversity support and a weaker reduction in progeny growth. This differs from ML015's I-F sign discordance and complements the existing primary systems without implying one universal layer ordering.

## Synthesis consequence

ML014 contributes **one independent primary cluster and two primary Hedges-g effects**. After admission, the primary denominator becomes **4 independent clusters / 11 primary effects**. ML015 remains a separate Fisher-z gradient-generalisation cluster and is not counted in that denominator.
