# ML004 / PS015 Conospermum 2020 cluster-recovery contract

## Goal

Attempt to recover one additional independent multilayer cluster from Delnevo et al. (2020), *Biological Conservation* 252:108824, DOI `10.1016/j.biocon.2020.108824`, without changing the existing multilayer effect-unit rules.

Target layers:

- `I_interaction`: flower visitation rate;
- `F_reproductive_function`: pollen-limitation / pollen-quality limitation response.

The target design is an eleven-population fragmentation gradient.

## Admission rule

ML004 is promoted only if **both** I and F can be represented on the same independent population frame and against the **same predeclared fragmentation exposure**.

Preferred common exposure, in order fixed before value extraction:

1. source-defined population connectivity/isolation metric if available for both layers;
2. source-defined population size if available for both layers;
3. source-defined floral-display index only if the paper explicitly treats it as the common fragmentation/resource exposure for both endpoints.

Do not select whichever predictor yields the strongest same-sign pattern after coefficients are seen.

## Accepted effect representations

A layer can enter the primary gradient stream only if one of the following is recoverable without post-hoc reconstruction:

1. population-level raw values paired with the fixed exposure, allowing a source-scale correlation/regression effect and sampling variance to be reconstructed;
2. a source model coefficient plus SE/CI for the fixed exposure and endpoint;
3. an exact source test statistic that has a preregistered, one-to-one conversion to the locked effect stream.

Ranges, endpoint percentages at selected predictor values, p-values alone, verbal significance, or plotted fitted lines without recoverable population/model uncertainty are insufficient.

## Dependence rule

I and F belong to one cluster, not two studies. If both are admitted, within-cluster covariance must be represented by one of:

- covariance reconstructed from paired population-level residual/effect contributions;
- source-reported model covariance;
- a transparent working covariance proxy from paired independent population values, with positive-definite audit.

Covariance must not silently be set to zero.

## Source recovery order

1. Delnevo 2020 thesis repository and full thesis chapter corresponding to the Biological Conservation paper;
2. ECU/UWA repository attachments or research datasets explicitly linked to that chapter/paper;
3. Elsevier supplementary package for PII `S000632072030882X`;
4. author-deposited tables/data linked from the thesis or institutional repository.

The 2019 Dryad dataset `10.5061/dryad.4cg374r` is a different publication/campaign and cannot be row-joined into PS015 merely because the species/populations overlap. It may be used only to identify source variable definitions or programme provenance unless the thesis explicitly establishes exact shared observations/campaign and the cluster contract is amended before fitting.

## Stop / no-rescue rules

Do not:

- infer Fisher z from the reported `1.3% -> 5.6%` or `1.5% -> 74.3%` ranges;
- convert a p-value alone into an effect;
- digitize a favourable fitted line after seeing its direction;
- combine 2019 reproductive observations with 2020 visitation observations as if synchronized without explicit source evidence;
- treat flowers, visits, experimental branches or treatment replicates as fragmentation-population `n`;
- switch exposure from connectivity to floral display or population size because another exposure is weak;
- promote only I or only F as a two-layer cluster.

Possible terminal outcomes:

- `ML004_admitted_I_F_covariance_aware`;
- `partial_single_layer_recovered_cluster_not_admitted`;
- `common_exposure_not_reconstructable`;
- `effect_unit_or_variance_not_reconstructable`;
- `source_access_blocked`.

All terminal outcomes are acceptable.
