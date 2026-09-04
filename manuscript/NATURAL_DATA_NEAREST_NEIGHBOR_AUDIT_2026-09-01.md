# Natural-data four-gate nearest-neighbour audit — 2026-09-01

## Purpose

This audit fixes the novelty boundary for the independent natural-data paper before full manuscript drafting. The paper must not claim novelty for ecological indicator validation, proxy selection, cross-validation, uncertainty partitioning, or variable standardisation by themselves. Its candidate contribution is the ordered and fail-closed coupling of those concerns before residual context is interpreted, demonstrated across locked natural datasets without pooling incompatible ecological effects.

## Closest methodological neighbours

### 1. Environmental and ecological indicator validation is established

Bockstaller & Girardin (2003, *Agricultural Systems*, doi:10.1016/S0308-521X(02)00053-7) explicitly distinguish design validation, output validation, and end-use validation for environmental indicators. This is a direct prior-art anchor: the present paper is not the first to argue that indicators require validation at more than one level.

The 2018 *Ecological Indicators* paper “The need for validation of ecological indices” likewise argues that indicators and aggregated indices require explicit validation because their behaviour can be counterintuitive. The present manuscript must therefore avoid any firstness claim for indicator validation as a scientific task.

Kershner et al. (2011/2019 framework lineage; “Scrupulous proxies”, *Ecological Indicators* 104:737–754, doi:10.1016/j.ecolind.2019.01.031) provides a rigorous framework for selecting and evaluating ecological indicator suites, including redundancy among indicators. This is especially close to the paper’s residual-redundancy branch.

Recent *Ecological Indicators* work continues this tradition. For example, generic proxies for grassland ecosystem properties are explicitly evaluated for their suitability as practical indicators (2024, volume 158, 111586), while recent monitoring syntheses operationalise biodiversity indicators using relevance, credibility, scalability and data-readiness criteria. The target journal is therefore already comfortable with papers that ask whether proposed ecological measures deserve indicator status.

### 2. Predictive validation and held-out testing are established

Predictive validation of ecological and environmental models predates this programme. Classical work emphasises that in-sample fit does not guarantee predictive validity, and later ecological papers advocate explicit prediction testing with held-out observations when independent validation data are unavailable.

The present paper therefore does not claim novelty for leave-one-site, leave-one-garden, leave-one-population, leave-one-orchard, leave-one-array, or leave-one-maternal-plant-out evaluation. Those designs are the evidence discipline used to evaluate the frozen candidate state/proxy in each system.

### 3. Indicator uncertainty and error partitioning are established

Recent work in *Ecological Indicators* shows that indicator confidence depends on correctly partitioning sampling and analytical uncertainty (“Getting the errors right”, 2024, volume 167, 112637). The present paper is not the first to argue that analytical processing can affect indicator reliability.

Its narrower contribution is to make information-preserving representation an explicit gate: a biological measurement that is mechanistically richer in raw units cannot support a richer state claim if preprocessing maps it onto the same analytical coordinate as the simpler proxy.

### 4. Standardisation and scaling are standard statistical tools

Schielzeth (2010, *Methods in Ecology and Evolution*, doi:10.1111/j.2041-210X.2010.00012.x) discusses predictor standardisation as a useful device for interpretation and comparison of regression effects. Scaling and centring are ordinary statistical operations, not a novel problem discovered here.

The *Campanula americana* result must therefore be described as a concrete representation-collapse case: because one candidate coordinate was a constant positive rescaling of another, feature-wise standardisation removed the multiplier that carried the intended mechanistic distinction. The novelty claim is not “standardisation is bad”; it is that representation preservation must be checked before a biologically richer measurement is credited as a distinct ecological state coordinate.

### 5. Indicator suites can be redundant or contradictory

Recent biodiversity-indicator work explicitly studies redundancy, corroboration and contradiction among indicators. The present paper therefore cannot claim firstness for detecting redundancy among ecological measures.

The distinct question here is sequential: after an endpoint-relevant biological state has been supplied, does additional geography, habitat, origin or history add transferable predictive information? A negative answer is only a residual-context result; it is not evidence that the biological state is complete or that the contextual variable is irrelevant.

## Candidate contribution that survives the audit

The strongest defensible contribution is an ordered empirical interpretation rule:

> **Test the state before interpreting the residual.**

The rule has four separable obligations:

1. **Measurement adequacy:** the proposed state/proxy must earn endpoint-relevant predictive status under the frozen held-out design.
2. **Representation preservation:** the analytical representation must preserve the biological distinction the richer measurement was intended to add.
3. **Residual-context test:** only after upstream state measurement is interpretable may geography, habitat, origin or history be tested as residual information.
4. **Cross-study identifiability:** synthesis stops when study, origin, taxa, protocol and response construction cannot be separated.

The empirical contribution is not one cross-system effect size. It is that locked natural analyses occupy distinct branches of this same interpretation workflow:

- residual context adds no detected transferable gain after an informative partial state;
- a contemporary process coordinate remains missing;
- a plausible process proxy fails to earn endpoint-relevant adequacy;
- preprocessing erases the intended mechanistic distinction;
- a requested cross-origin synthesis remains not identifiable.

This produces a paper about **what can be interpreted next**, rather than a meta-analysis of whether one ecological driver matters.

## Novelty firewall

Do **not** claim:

- first framework for validating ecological indicators;
- first use of predictive or cross-validation for ecological models;
- first framework for selecting ecological proxies;
- first observation that indicator uncertainty has sampling and analytical components;
- first warning that scaling or standardisation changes statistical representation;
- first demonstration that indicator suites can be redundant;
- one universal law connecting island, urban, pollination or mating systems.

Safe contribution language:

> We connect endpoint-relevant state measurement, information-preserving representation, residual-context testing and cross-study identifiability in one fail-closed interpretation sequence, and show with prospectively frozen or locked natural-data analyses that its branches yield scientifically different next-step decisions.

## Venue fit after the literature audit

### Ecological Indicators — primary

The current Elsevier scope describes *Ecological Indicators* as integrating ecological/environmental monitoring and assessment with management, and explicitly includes new indicators, new approaches and methods for indicator development, testing and use. It also states that simple descriptive single-case monitoring without methodological or indicator-development insight is not sufficient. The proposed four-gate synthesis fits if it is written as a reusable indicator/state-evaluation logic supported by multiple natural systems, not as seven unrelated case studies.

### Methods in Ecology and Evolution — conditional stretch only

The current MEE scope emphasises new methods and methodological approaches rather than results of applying existing methods. Its author guidance also states that computational methods normally should be tested with simulations or benchmark datasets, and that workflows linking existing methods generally are not considered new methods. Therefore the present empirical synthesis should not be sent to MEE merely by renaming the gate logic a “method”. MEE becomes credible only after a separate development branch supplies a reusable implementation and truth-known simulation/benchmark evaluation.

## Manuscript consequence

The main text should cite the validation/proxy literature early, concede that the component practices are established, and then make the ordered interpretation problem explicit. The paper should be organised by gate outcome rather than organism and should never pool the locked within-study contrasts onto one ecological effect-size axis.
